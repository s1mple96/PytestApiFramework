"""
@FileName: $
@Auther: s1mple
@Description: ...
"""
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s -- %(levelname)s -- %(filename)s -- %(message)s')
logger = logging.getLogger(__name__)