#!/usr/bin/env python3
"""
Unit tests for TopicInfo selected QoS subscription behavior.

This test does not require a running ROS graph. It directly instantiates
TopicInfo and verifies that the selected QoS profile is passed directly to
the subscription.

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

from rclpy.qos import QoSProfile, ReliabilityPolicy

# Import after path manipulation
from rqt_topic.topic_info import TopicInfo


class TestTopicInfoSelectedQos:

    def test_start_monitoring_uses_selected_qos_profile(self):
        """start_monitoring must pass the selected QoS profile directly."""
        node = MagicMock()
        topic_info = TopicInfo(node, '/test_topic', 'std_msgs/String')
        qos_profile = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)
        topic_info.set_qos_profile(qos_profile)

        # message_class should be resolved for std_msgs/String
        assert topic_info.message_class is not None

        topic_info.start_monitoring()

        assert topic_info.monitoring is True
        node.create_subscription.assert_called_once()
        call_kwargs = node.create_subscription.call_args.kwargs
        assert call_kwargs['qos_profile'] is qos_profile
        assert 'qos_overriding_options' not in call_kwargs

    def test_set_qos_profile_recreates_active_subscription(self):
        """Changing QoS while checked must destroy and recreate the subscription."""
        node = MagicMock()
        topic_info = TopicInfo(node, '/test_topic', 'std_msgs/String')

        topic_info.start_monitoring()
        replacement_qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)
        topic_info.set_qos_profile(replacement_qos)

        assert topic_info.monitoring is True
        assert node.create_subscription.call_count == 2
        node.destroy_subscription.assert_called_once()
        call_kwargs = node.create_subscription.call_args.kwargs
        assert call_kwargs['qos_profile'] is replacement_qos

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
