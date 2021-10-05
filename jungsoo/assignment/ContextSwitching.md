# ContextSwitching

- Computer가 매번 하나의 Task만 처리할 수 있다면
반응속도가 매우 느리고 사용하기 불편.
    
    ⇒ 많은 사람들이 동시에 사용하는 것처럼 보여지기 위해 Context Switching을 사용합니다.
    

### Context Switching이란?

- 현재 진행되고 있는 Task(Process, Thread)의 상태를 저장하고
다음 진행할 Task의 상태 및 Register 값들에 대항 정보(Context)를 읽어 교체하는 과정.
- 빠른 속도로 Task를 바꿔 가며 실행하기 때문에 사람의 눈으로는 실시간처럼 보이게 되는 장점이 존재.

### 진행 과정

- Task의 대부분 정보는 Register에 저장되고 Process Control Block(PCB)으로 관리되고 있다.
- 현재 실행하고 있는 Task의 PCB 정보를 저장.
- 다음 실행할 Task의 PCB 정보를 읽어 Register에 적재, CPU가 이전에 진행했던 과정을 연속적으로 수행 가능.

1. 프로그램(실행파일) 실행
2. 프로세스(프로그램의 인스턴스) 생성
3. 프로세스 주소 공간에 코드, 데이터, 스택 생성
4. 해당 프로세스의 Metadata들이 PCB에 저장.

## Cost

- Cache 초기화
- Memory Mapping 초기화
- 항상 실행되어야 하는 Kernel

⇒ 잦은 Context Switching은 성능 저하를 가져온다.

- Register란?
    - CPU가 요청을 처리하는게 필요한 데이터를 일시적으로 저장하는 기억장치
    - 데이터를 영구 저장 → 하드디스크 / 임시 저장 → RAM
    - 하지만 저장 명령을 처리하기 위해 이들의 주소와 명령 종류를 저장할 수 있는 기억 공간이 더 필요.
    - CPU 자체적으로 데이터를 저장할 수 없기에 CPU와 직접적으로 연결시켜 위 역할을 수행하는 곳이 Register이다.
    - 32비트, 64비트 시스템이란 것이
    "명령을 한 번에 처리할 수 있는 레지스터의 비트 수"이다.
    
- PCB란?
    - 프로세스들의 특징을 갖고 있는 것 ⇒ Process Metadata
        
        (프로세스 고유 식별 번호, 상태, 스케줄링 정보(우선순위 등), Register 등)
        
    - 이러한 Metadata는 process가 생성되면 Process control Block라는 곳에 저장.
    

## 참고 사이트

[컨텍스트 스위치(Context Switching) 에 대한 정리](https://jins-dev.tistory.com/entry/%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8-%EC%8A%A4%EC%9C%84%EC%B9%98Context-Switching-%EC%97%90-%EB%8C%80%ED%95%9C-%EC%A0%95%EB%A6%AC)

[[운영체제] 레지스터란?](http://itnovice1.blogspot.com/2019/08/blog-post_99.html)

[[OS] PCB와 Context Switching](https://m.blog.naver.com/adamdoha/222019884898)

[[OS] Lecture 3. Process Management (1/2) / 운영체제 강의](https://www.youtube.com/watch?v=jZuTw2tRT7w&list=PLBrGAFAIyf5rby7QylRc6JxU5lzQ9c4tN&index=6)

[프로세스, 프로세서(CPU), Context Switching, 스레드, 멀티스레드](https://darrengwon.tistory.com/763)

- 한 프로그램이 실행하기 위해 하나의 프로세스만으로 부족하게 되었.
- 프로세스 내부에 실행하는 단위를 쪼개는 '스레드'를 이용하게 되면서 CS의 비용을 줄일 수 있게 됨.

## 멀티 스레드

1. 장점
    - Stack 영역을 제외한 메모리를 서로 공유하기 때문에 "응답시간이 빨라"지고 "메모리도 아낄" 수 있다.
2. 단점
    - 한 스레드가 오류가 났을 경우 프로세스 전체가 종료.
    - 자원을 공유하기 대문에 동기화 문제도 발생
    - 순차적으로 실행될 것을 보장 X

## 정리

- 멀티 프로세스
    1. 프로세스를 바꿔서 실행
    2. Context Switching이 일어나면서 전환
    3. 자주 실행되지 않도록 적절한 알고리즘 개발이 관건.
    
- 멀티 스레드
    1. 프로세스간 통실 줄이고, Context Switching 비용을 줄이기 위해 여러 스레드 구성.
    2. 그러나 Stack 영역에 대한 Context Swiching 비용은 그대로.