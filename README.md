# GATask
This program assigns h/w resources for a task using GA to optimize power 

## Input
자세한 내용은 파일 내부의 설명을 참고하세요.
- input_mem.txt: 메모리의 종류, 종류 별 실행률, 용량, active 상태의 전력소모량, idle 상태의 전력소모량 
- input_processer.txt: 프로세서의 코어 개수, voltage/frequency 모드의 개수, 모드 별 실행률, active 상태의 전력소모량, idle 상태의 전력소모량
- input_tasks.txt: 태스크의 개수, 태스크 별 최악수행시간, 주기, 메모리 요구량
- input_other.txt: 최대 세대수, 솔루션 셋의 솔루션 수, 허용 utilization, PENALTY_RATIO, 돌연변이 발생 확률, Roulette-wheel selection의 상수 k, ranking selection에서 사용할 상수 MAX, MIN

## Run
정보를 위 input 파일에 형식을 맞추어 입력하고, Main.py를 실행한다.<br>

## Output
최종 솔루션셋의 솔루션 중 가장 전력 소모량이 적은 솔루션이 result.txt로 출력된다.
각 줄마다 input_tasks의 task에 하나씩 대응하며, 프로세서의 voltage/frequency 모드와 메모리 종류 순으로 출력된다.

## Demo
GA Demo: 10000세대 진화 결과
https://youtu.be/aSAMVM6kDyg
