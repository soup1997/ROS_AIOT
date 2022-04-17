# 개발환경
|Platform|Controller|Version|  
|------|---|---|
|**Hanback electronics AIOT** ![17801b61bc9549bf3c87573db98124ac](https://user-images.githubusercontent.com/86957779/163716288-54f3a271-0dc5-4a75-902b-0936ce2f8ac8.jpg)|Jetson Xavier NX|Ubuntu18.04 LTS, ROS Melodic|  


# IMU값을 받아오기 위한 python library smbus이용 
![image](https://user-images.githubusercontent.com/86957779/159165886-1cf1ae51-df86-4939-94c9-626fc5b58701.png)   
![image](https://user-images.githubusercontent.com/86957779/159165966-e4577683-e1a6-448c-9a49-3aa6dccf5a78.png)   
  * Laser scan mather node는 LiDAR데이터와 IMU 데이터를 받아 실제공간과 매치 유사도를 측정   
  * Map Server의 경우 Hector SLAM을 이용하여 미리 만들어 놓은 맵 파일    
![image](https://user-images.githubusercontent.com/86957779/159166048-52339e53-4b6f-4316-9fa2-2defe0e40a1f.png) SLAM을 이용한 연구실 지도 (MAP)
![image](https://user-images.githubusercontent.com/86957779/159166125-87b95dff-f5fb-4112-bed7-49489bd66999.png)
  * 빨간색 화살표는 현재 추정 위치(current pose)를 나타냄
  * 보라색 화살표는 IMU의 Yaw값을 나타냄

# Result
![image](https://user-images.githubusercontent.com/86957779/159166171-d1769e71-cbe3-4ee0-b28e-ef3412275100.png)
  * Map Server에서 SLAM으로 작성한 Map을 AMCL에 제공
  * RplidarNode에서 AMCL에 /LaserScan, /Pointcloud2 제공
  * move_base는 스캔정보와, global planner, local planner를 통합하여 최종 출력정보로 선속도와 각속도인 cmd_vel 메시지 출력        
# Problems
  1. 엔코더가 장착되지 않아 라이다에 매우 의존적
  2. 이로인해 로봇이 이동할 경우 현재 위치 추정치가 발산하여 Localization결과와 매우 큰 위치오차 발생
  3. AMCL은 PointCloud와 모터 엔코터 ticks(Pulse)정보를 토대로 정확한 Localization이 가능함. 
