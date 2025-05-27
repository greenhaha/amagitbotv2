"""
知识库管理器
实现基于向量检索的知识存储和检索功能
"""
import uuid
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from core.config import settings
from core.logger import logger


class KnowledgeItem:
    """知识项目"""
    def __init__(
        self,
        content: str,
        metadata: Dict[str, Any] = None,
        item_id: str = None,
        timestamp: datetime = None
    ):
        self.id = item_id or str(uuid.uuid4())
        self.content = content
        self.metadata = metadata or {}
        self.timestamp = timestamp or datetime.now()


class KnowledgeBase:
    """知识库管理器"""
    
    def __init__(self, collection_name: str = "chatbot_knowledge"):
        self.collection_name = collection_name
        
        # 初始化ChromaDB
        self.chroma_client = chromadb.PersistentClient(
            path=settings.chroma_persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # 初始化句子转换器
        try:
            self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("句子转换器加载成功")
        except Exception as e:
            logger.error(f"句子转换器加载失败: {e}")
            # 使用备用模型
            self.encoder = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        
        # 获取或创建集合
        try:
            self.collection = self.chroma_client.get_collection(collection_name)
            logger.info(f"加载现有知识库集合: {collection_name}")
        except:
            self.collection = self.chroma_client.create_collection(
                name=collection_name,
                metadata={"description": "Chatbot knowledge base"}
            )
            logger.info(f"创建新知识库集合: {collection_name}")
    
    def add_knowledge(
        self, 
        content: str, 
        metadata: Dict[str, Any] = None,
        user_id: str = None,
        session_id: str = None
    ) -> str:
        """
        添加知识到知识库
        
        Args:
            content: 知识内容
            metadata: 元数据
            user_id: 用户ID
            session_id: 会话ID
            
        Returns:
            str: 知识项目ID
        """
        try:
            # 创建知识项目
            knowledge_item = KnowledgeItem(content=content, metadata=metadata)
            
            # 生成向量嵌入
            embedding = self.encoder.encode([content])[0].tolist()
            
            # 准备元数据
            item_metadata = {
                "user_id": user_id,
                "session_id": session_id,
                "timestamp": knowledge_item.timestamp.isoformat(),
                "content_type": "conversation",
                **(metadata or {})
            }
            
            # 添加到ChromaDB
            self.collection.add(
                embeddings=[embedding],
                documents=[content],
                metadatas=[item_metadata],
                ids=[knowledge_item.id]
            )
            
            logger.info(f"添加知识到知识库: {content[:50]}...")
            return knowledge_item.id
            
        except Exception as e:
            logger.error(f"添加知识失败: {e}")
            raise
    
    def search_knowledge(
        self, 
        query: str, 
        n_results: int = 5,
        user_id: str = None,
        filter_metadata: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        搜索相关知识
        
        Args:
            query: 查询文本
            n_results: 返回结果数量
            user_id: 用户ID（用于过滤）
            filter_metadata: 过滤条件
            
        Returns:
            List[Dict[str, Any]]: 搜索结果列表
        """
        try:
            # 生成查询向量
            query_embedding = self.encoder.encode([query])[0].tolist()
            
            # 构建过滤条件
            where_clause = {}
            if user_id:
                where_clause["user_id"] = user_id
            if filter_metadata:
                where_clause.update(filter_metadata)
            
            # 执行搜索
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where_clause if where_clause else None,
                include=["documents", "metadatas", "distances"]
            )
            
            # 格式化结果
            formatted_results = []
            if results["documents"] and results["documents"][0]:
                for i, doc in enumerate(results["documents"][0]):
                    formatted_results.append({
                        "content": doc,
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                        "similarity": 1 - results["distances"][0][i] if results["distances"] else 0.0
                    })
            
            logger.info(f"知识搜索完成，找到 {len(formatted_results)} 个相关结果")
            return formatted_results
            
        except Exception as e:
            logger.error(f"知识搜索失败: {e}")
            return []
    
    def get_conversation_context(
        self, 
        user_id: str, 
        session_id: str = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        获取对话上下文
        
        Args:
            user_id: 用户ID
            session_id: 会话ID
            limit: 限制数量
            
        Returns:
            List[Dict[str, Any]]: 上下文列表
        """
        try:
            where_clause = {"user_id": user_id}
            if session_id:
                where_clause["session_id"] = session_id
            
            # 获取最近的对话记录
            results = self.collection.query(
                query_embeddings=None,
                n_results=limit,
                where=where_clause,
                include=["documents", "metadatas"]
            )
            
            context = []
            if results["documents"] and results["documents"][0]:
                for i, doc in enumerate(results["documents"][0]):
                    metadata = results["metadatas"][0][i] if results["metadatas"] else {}
                    context.append({
                        "content": doc,
                        "timestamp": metadata.get("timestamp"),
                        "metadata": metadata
                    })
            
            # 按时间排序
            context.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            
            return context
            
        except Exception as e:
            logger.error(f"获取对话上下文失败: {e}")
            return []
    
    def add_conversation_turn(
        self,
        user_message: str,
        assistant_response: str,
        user_id: str,
        session_id: str,
        emotion_info: Dict[str, Any] = None
    ) -> Tuple[str, str]:
        """
        添加对话轮次到知识库
        
        Args:
            user_message: 用户消息
            assistant_response: 助手回复
            user_id: 用户ID
            session_id: 会话ID
            emotion_info: 情感信息
            
        Returns:
            Tuple[str, str]: 用户消息ID和助手回复ID
        """
        try:
            # 添加用户消息
            user_metadata = {
                "role": "user",
                "emotion": emotion_info.get("emotion") if emotion_info else None,
                "emotion_confidence": emotion_info.get("confidence") if emotion_info else None
            }
            
            user_id_result = self.add_knowledge(
                content=user_message,
                metadata=user_metadata,
                user_id=user_id,
                session_id=session_id
            )
            
            # 添加助手回复
            assistant_metadata = {
                "role": "assistant"
            }
            
            assistant_id_result = self.add_knowledge(
                content=assistant_response,
                metadata=assistant_metadata,
                user_id=user_id,
                session_id=session_id
            )
            
            logger.info(f"对话轮次已添加到知识库")
            return user_id_result, assistant_id_result
            
        except Exception as e:
            logger.error(f"添加对话轮次失败: {e}")
            return None, None
    
    def get_relevant_memories(
        self,
        current_message: str,
        user_id: str,
        n_results: int = 3
    ) -> List[Dict[str, Any]]:
        """
        获取与当前消息相关的记忆
        
        Args:
            current_message: 当前消息
            user_id: 用户ID
            n_results: 返回结果数量
            
        Returns:
            List[Dict[str, Any]]: 相关记忆列表
        """
        try:
            # 搜索相关的历史对话
            relevant_memories = self.search_knowledge(
                query=current_message,
                n_results=n_results,
                user_id=user_id
            )
            
            # 过滤掉相似度太低的结果
            filtered_memories = [
                memory for memory in relevant_memories 
                if memory["similarity"] > 0.3
            ]
            
            logger.info(f"找到 {len(filtered_memories)} 个相关记忆")
            return filtered_memories
            
        except Exception as e:
            logger.error(f"获取相关记忆失败: {e}")
            return []
    
    def summarize_session(
        self,
        user_id: str,
        session_id: str
    ) -> Optional[str]:
        """
        总结会话内容
        
        Args:
            user_id: 用户ID
            session_id: 会话ID
            
        Returns:
            Optional[str]: 会话总结
        """
        try:
            # 获取会话中的所有对话
            context = self.get_conversation_context(
                user_id=user_id,
                session_id=session_id,
                limit=50
            )
            
            if not context:
                return None
            
            # 简单的总结逻辑（实际应用中可以使用LLM进行总结）
            total_messages = len(context)
            user_messages = [c for c in context if c.get("metadata", {}).get("role") == "user"]
            assistant_messages = [c for c in context if c.get("metadata", {}).get("role") == "assistant"]
            
            # 提取关键词（简化版本）
            all_content = " ".join([c["content"] for c in context])
            words = all_content.split()
            
            summary = f"会话包含 {total_messages} 条消息，其中用户消息 {len(user_messages)} 条，助手回复 {len(assistant_messages)} 条。"
            
            return summary
            
        except Exception as e:
            logger.error(f"总结会话失败: {e}")
            return None
    
    def delete_knowledge(self, knowledge_id: str) -> bool:
        """
        删除知识项目
        
        Args:
            knowledge_id: 知识项目ID
            
        Returns:
            bool: 是否成功
        """
        try:
            self.collection.delete(ids=[knowledge_id])
            logger.info(f"删除知识项目: {knowledge_id}")
            return True
            
        except Exception as e:
            logger.error(f"删除知识项目失败: {e}")
            return False
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """
        获取知识库统计信息
        
        Returns:
            Dict[str, Any]: 统计信息
        """
        try:
            count = self.collection.count()
            return {
                "total_items": count,
                "collection_name": self.collection_name
            }
            
        except Exception as e:
            logger.error(f"获取统计信息失败: {e}")
            return {"total_items": 0, "collection_name": self.collection_name} 