#!/usr/bin/env python3
"""
Unit test for TopicInfo QoS override callback.

This test does not require a running ROS graph. It directly instantiates
TopicInfo and verifies that the qos_callback method exists and behaves
correctly.

Usage:
    cd /path/to/rqt_topic
    python3 -m pytest scripts/test_topic_info_qos.py -v
"""

import sys
import os

# Ensure src/ is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from unittest.mock import MagicMock

# Import after path manipulation
from rqt_topic.topic_info import TopicInfo


class TestTopicInfoQosOverride:

    def test_qos_callback_exists(self):
        """Ensure qos_callback method is present on TopicInfo."""
        node = MagicMock()
        topic_info = TopicInfo(node, '/test_topic', 'std_msgs/String')
        assert hasattr(topic_info, 'qos_callback')

    def test_qos_callback_returns_success(self):
        """qos_callback must return a result with successful=True."""
        node = MagicMock()
        topic_info = TopicInfo(node, '/test_topic', 'std_msgs/String')
        result = topic_info.qos_callback(None)
        assert result.successful is True

    def test_start_monitoring_passes_qos_overriding_options(self):
        """start_monitoring must pass qos_overriding_options to create_subscription."""
        node = MagicMock()
        topic_info = TopicInfo(node, '/test_topic', 'std_msgs/String')

        # message_class should be resolved for std_msgs/String
        assert topic_info.message_class is not None

        topic_info.start_monitoring()

        assert topic_info.monitoring is True
        node.create_subscription.assert_called_once()
        call_kwargs = node.create_subscription.call_args.kwargs
        assert 'qos_overriding_options' in call_kwargs

    def test_stop_monitoring_cleans_up(self):
        """stop_monitoring must destroy the subscription."""
        node = MagicMock()
        topic_info = TopicInfo(node, '/test_topic', 'std_msgs/String')
        topic_info.start_monitoring()
        topic_info.stop_monitoring()
        assert topic_info.monitoring is False
        assert topic_info._subscriber is None
        node.destroy_subscription.assert_called_once()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
