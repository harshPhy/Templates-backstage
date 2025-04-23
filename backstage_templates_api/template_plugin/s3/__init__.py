"""
S3 Module

This module provides functionality for interacting with AWS S3.
"""

from template_plugin.s3.client import S3Client
from template_plugin.s3.downloader import S3Downloader

__all__ = ['S3Client', 'S3Downloader'] 