

## 프로세스와 스레드의 차이

### 프로세스

* `실행중인 프로그램`
* 운영체제로부터 자원을 할당받아 실행
* `코드/데이터/스택/힙` 메모리 영역

### 스레드 

* 프로세스의 실행 단위
* 프로세스의 코드/데이터/힙 메모리 영역을 공유하고 `개별적인 스택`을 가짐
* 스택을 공유하는 이유? - 독립적인 함수호출 - 독립적인 실행 흐름을 추가하는 조건이지

## 멀티 프로세싱과 멀티 스레딩

- 멀티 코어 환경은 `공유 자원(Cirical Section)`이 있을 시 동기화 매커니즘이 필요

###  멀티 프로세싱

- 다수의 프로세서(CPU)가 여러 작업을 동시에 처리하는 것 (병렬 처리)
- Pipe나 Shared Memory가 있어야 데이터를 주고 받을 수 있음
- `많은 메모리 공간`을 차지
- `IPC라는 별도 매커니즘`을 사용
- 프로세스 간의 통신 비용/문맥 교환 `비용이 큼`
- 안전성: 하나의 프로세스가 죽더라도 다른 프로세스에는 영향을 끼치지 않고 정상적으로 수행

### 멀티 스레딩

- 하나의 프로세스에 여러 스레드로 자원을 공유하며 작업을 나누어 수행하는 것
- 스레드 간은 `데이터/힙 영역을 공유`하므로 Shared Memory가 없어도 데이터를 주고 받을 수 있음
- `적은 메모리 공간`을 차지
- 프로세스를 생성하여 자원을 할당하는 시스템 콜이 감소함으로서 `자원을 효율적으로 관리`
- 스레드 간의 통신 비용과 문맥 교환 `비용이 적음`
- 하나의 스레드의 비정상적인 활동은 전체 스레드에 영향을 끼칠 수 있음

### 뮤텍스와 세마포어의 차이

- 뮤텍스(Mutex)

  - 공유된 자원의 데이터를 **여러 프로세스 혹은 스레드가** 접근하는 것을 막는 것
  - 상호배제라고도 하며, Critical Section을 가진 스레드의 Running time이 서로 겹치지 않도록 각각 단독으로 실행하게 하는 기술이다.
  - 다중 프로세스들의 공유 리소스에 대한 접근을 조율하기 위해 synchronized 또는 lock을 사용한다.
    - 즉, 뮤텍스 객체를 두 스레드가 동시에 사용할 수 없다.

- 세마포어(Semaphore)

  - 공유된 자원의 데이터를 **여러 프로세스 혹은 스레드가** 접근하는 것을 막는 것

  - 리소스 상태를 나타내는 간단한 카운터로 생각할 수 있다.

    - 운영체제 또는 커널의 한 지정된 저장장치 내의 값이다.
    - 일반적으로 비교적 긴 시간을 확보하는 리소스에 대해 이용한다.
    - 유닉스 시스템 프로그래밍에서 세마포어는 운영체제의 리소스를 경쟁적으로 사용하는 다중 프로세스에서 행동을 조정하거나 또는 동기화 시키는 기술이다.

  - 공유 리소스에 접근할 수 있는 프로세스의 최대 허용치만큼 동시에 사용자가 접근하여 사용할 수 있다.

  - 각 프로세스는 세마포어 값은 확인하고 변경할 수 있다.

    - 1. 사용 중이지 않는 자원의 경우 그 프로세스가 즉시 자원을 사용할 수 있다.

    - 1. 이미 다른 프로세스에 의해 사용 중이라는 사실을 알게 되면 재시도하기 전에 일정 시간을 기다려야 한다.

      세마포어를 사용하는 프로세스는 그 값을 확인하고, 자원을 사용하는 동안에는 그 값을 변경함으로써 다른 세마포어 사용자들이 기다리도록 해야한다.

  - 세마포어는 이진수 (0 또는 1)를 사용하거나, 또는 추가적인 값을 가질 수도 있다.

- 차이

  1. 가장 큰 차이점은 관리하는

     동기화 대상의 개수

     - Mutex는 동기화 대상이 오직 하나뿐일 때, Semaphore는 동기화 대상이 하나 이상일 때 사용한다.

  2. Semaphore는 Mutex가 될 수 있지만 Mutex는 Semaphore가 될 수 없다.

     - Mutex는 상태가 0, 1 두 개 뿐인 binary Semaphore

  3. Semaphore는 소유할 수 없는 반면, Mutex는 소유가 가능하며 소유주가 이에 대한 책임을 가진다.

     - Mutex 의 경우 상태가 두개 뿐인 lock 이므로 lock 을 가질 수 있다.

  4. Mutex의 경우 Mutex를 소유하고 있는 스레드가 이 Mutex를 해제할 수 있다. 하지만 Semaphore의 경우 이러한 Semaphore를 소유하지 않는 스레드가 Semaphore를 해제할 수 있다. 시그널로

  5. Semaphore는 시스템 범위에 걸쳐있고 파일시스템상의 파일 형태로 존재하는 반면 Mutex는 프로세스 범위를 가지며 프로세스가 종료될 때 자동으로 Clean up 된다.



Round robin 이 뭐냐?

-> 주의점

-> 컨텍스트 스위칭 얘기가 나옴

-> PCB  뭐가 저장되냐

-> program counter



pcb를 가지듯이 스레드도 비슷한 역할을 하는 - thread마다 pc 레지스터를 가져야한다

https://vsfe.tistory.com/12

스레드가 할당받는 자원의 양이 적어서

멀티스레드 멀티 프로세스 장단차이



프로세스 동기화에서 공유자원에 접근했을 때 ? 생기는 문제

레이스 컨디션 -> 방법 -> 뮤텍스 세마포어 -> 데드락 ? 

- 교착상태의 4가지 조건

  1. 상호 배제(mutual exclusion)

     - 한 번에 한 프로세스만 공유 자원을 사용할 수 있다.
     - 좀 더 정확하게는, 공유 자원에 대한 접근 권한이 제한된다. 자원의 양이 제한되어 있더라도 교착상태는 발생할 수 있다.

  2. 들고 기다리기(hold and wait) =

     점유대기

     - 공유 자원에 대한 접근 권한을 갖고 있는 프로세스가, 그 접근 권한을 양보하지 않은 상태에서 다른 자원에 대한 접근 권한을 요구할 수 있다.

  3. 선취(preemption) 불가능 =

     비선점

     - 한 프로세스가 다른 프로세스의 자원 접근 권한을 강제로 취소할 수 없다.

  4. 대기 상태의 사이클(circular wait) =

     순환대기

     - 두 개 이상의 프로세스가 자원 접근을 기다리는데, 그 관계에 사이클이 존재한다.

힙과 스텍의차이 스텍오버플로우

멀티 스레드가 무조건 좋냐?



시스템 콜은 cpu 내부에서 발생하는 일읆 ㅏㄹ하는거

인터럽트는 cpu 외부에서 일어나는걸 



**시스템 호출과 인터럽트의 차이점은 무엇?**

시스템 호출은 시스템에 내장 된 서브 루틴에 대한 호출이고 인터럽트는 이벤트로 프로세서가 현재 실행을 일시적으로 유지하게합니다. 그러나 한 가지 주요 차이점은 시스템 호출은 동기식이지만 인터럽트는 그렇지 않다는 것입니다. 즉, 시스템 호출은 고정 된 시간 (일반적으로 프로그래머가 결정)에 발생하지만 사용자가 키보드를 누르는 것과 같은 예기치 않은 이벤트로 인해 언제든지 인터럽트가 발생할 수 있습니다.따라서 시스템 호출이 발생할 때마다 프로세서는 복귀 할 위치 만 기억하면되지만 인터럽트 발생시 프로세서는 복귀 할 위치와 시스템 상태를 모두 기억해야합니다. 시스템 호출과 달리 인터럽트는 일반적으로 현재 프로그램과 관련이 없습니다.



## PCB

> PC ( Program Counter) , SP (Stack Pointer) 는 어디에 저장?

Process Context Block

1. Process ID
2. Register - PC, SP
3. Scheduling info - Process State
4. Memory Info - memory size limit



## Context Switching

1. 실행 중지할 프로세스 정보를 해당 프로세스의 PCB에 업데이트 해서 메인 메모리에 저장
2. 다음 실행할 프로세스 정보를 메인 메모리에 있는 해당 PCB 정보를 CPU에 넣고 실행
   * PC, SP를 CPU의 레지스터에 넣고 실행

## IPC InterProcess Communication

프로세스는 다른 프로세스의 공간에 접근 불가

-> 어쨰서 접근 불가능한걸까? - 가상 메모리, mmu memory management unit

```
프로세스 격리의 기본 기능은 프로세스 또는 프로그램에 명확하게 정의 된 가상 주소 공간을 할당하는 것입니다. 이 공간에는 프로그램 및 모든 관련 데이터가 있습니다. 프로세스에 더 많은 공간이 필요한 경우 운영 체제에서 요청하고 사용 가능한 경우 할당됩니다. 이러한 방식으로 운영 체제는 두 프로세스가 우연히 또는 의도적으로 서로의 메모리에 액세스하는 것을 막을 수 있습니다.
```

커널 공간을 활용하는 것 - 커널 공간을 공유하니까

1. file
2. Message Queue
3. Shared Memory
4. Pipe
5. Signal
6. Semaphore
7. Socket

Bootstrap Program :

Rom 안에 저장 되어 있고 , First program( OS ) 를 파워가 켜지면 실행 한다.

시스템을 모두 initialization 해줌

그리고 OS 를 메모리에 올린다. 

Operating System : booting 프로세스가 다 실행 된 후

최초로 돌아가는 프로세스? scheduler.

걔가 첫번째 돌아가는 프로세스를 init으로 지정 해주는거 - pid 1 - init - 일반 프로세스의 조상



세마포어 IPC ? 

기본적으로 공유 메모리 하고 같이 쓰이는건가? - 공유메모리 공간을 동시에 접근이 어려우니까..

공유메모리 동작 방식?

공유멤리 -> 라이브러리를 공유메모리 방식으로 사용함 os가 라이브러리를 공유메모리부분에 적재시켜놓고 메모리를 아낌 -> 메모리에 접근하는 방식은 매핑테이블을 통해서 공유 메모리 공간에 접근이 가능함

커널에 공유메모리 공간을 요청하면, 공유메모리 공간을 접근할 수 있는 식별자를 얻고, 이 식별자로 접근이 가능하다

결국 세마포어도 얘가 접근이 가능한거다 아니다라는 통신을 제공하는건가?



엄연히 말하면 가상 메모리 - swap memory는 다른 얘기아닌가요?

mmu - Memory Management Unit

* 가상 주소 메모리 접근 시 물리 주소 값으로 변환해주는 하드웨어 장치



## 페이징 시스템

* 크기가 동일한 페이지로 가상 주소 공간과 이에 매칭하는 물리 주소 공간을 관리
* 하드웨어에서 지원해야함
* 페이지 번호를 기반으로 가상 주소/물리 주소 매핑 기록을 사용



요구 페이징 - demand paging / demanded paging

* 모든 데이터를 메모리로 적재하는 것이 아닌 필요한 시점에서만 메모리로 적재
* 선행 페이징으 반대 개념
* 더 필요하지 않은 페이지 프레임은 다시 저장 매체에 저장

FIFO - 

OPT imal Replacement Algorithm - 가장 오랫동안 사용하지 않을 페이지 내리자 , 

LRU - Least Recently Used  - 가장 오래전에 사용된 페이지를 교체 - 과거 기록 기반

LFU - Least Frequently Used - 가장 적게 사용된..

NUR - Not Used Recentrly









