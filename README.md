# ROS 2 Humble용 커스텀 rqt_topic

이 fork는 ROS 2 Humble에서 토픽별 subscriber QoS를 UI에서 직접 선택할 수 있도록 수정한 `rqt_topic`입니다.

기본 `rqt_topic`으로는 `BEST_EFFORT` 같은 기본값과 다른 QoS 토픽을
모니터링하기 어려울 때 이 버전을 사용합니다.

## 변경 사항

- 각 토픽 행에 `Reliability`, `History`, `Durability`, `Depth` 설정을 추가했습니다.
- 새 토픽이 표시될 때 첫 publisher의 QoS profile을 기본 선택값으로 사용합니다.
- 토픽을 이미 체크해서 구독 중인 상태에서도 QoS 설정을 바꾸면 subscription을 다시 생성합니다.
- UI에서 선택한 QoS profile을 subscription에 직접 사용합니다.
- 잘못된 QoS로 한 번 구독 실패한 뒤에도, 올바른 QoS로 바꾸고 다시 구독할 수 있습니다.

## Build

ROS 2 Humble을 native 환경에서 사용하고, workspace가 `~/ros2_ws`라고 가정합니다.

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone -b humble https://github.com/blu-y/rqt_topic.git
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select rqt_topic --symlink-install
source ~/ros2_ws/install/setup.bash
rm -rf ~/.config/ros.org/rqt_gui.ini
```

`rm -rf ~/.config/ros.org/rqt_gui.ini`는 기존 rqt GUI 설정을 삭제하는
단계입니다. 기존 `rqt_topic`의 header 상태가 남아 있으면 커스텀 빌드가
정상 적용되어도 새 QoS 컬럼이 보이지 않을 수 있습니다. 이 파일은 rqt가
다시 실행될 때 새 설정으로 재생성됩니다.

## Verify install

항상 `/opt/ros/humble/setup.bash`를 먼저 source하고, 그 다음 workspace overlay를 source해야 합니다.

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 pkg prefix rqt_topic
```

정상이라면 다음처럼 workspace 경로가 나와야 합니다.

```text
~/ros2_ws/install/rqt_topic
```

## Usage

새 터미널을 열 때마다 overlay 순서를 다시 맞춰야 합니다.

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
rqt --standalone rqt_topic
# 또는
# ros2 run rqt_topic rqt_topic
```
