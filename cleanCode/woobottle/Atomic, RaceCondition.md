### Atomic 
여러개의 스레드가 있을때 특정시점에 어떤 메소드를 두개 이상의 쓰레드가 동시에 호출 못한다.

```java
class Job implements Runnable {
  public void run() {
    while (true) {
      go();
      stop();
    }
  }

  public void go() {
    // 매우 중요한 작업
  }

  public void stop() {
    // 그냥 일반적인 작업
  }
}
```
main 클래스에서 Job 객체를 이용해서 여러개의 스레드를 생성 및 실행 시켰다.
이때 1번 스레드가 `go()` 를 실행 중인데 2번 스레드가 `go()` 를 실행 시킬 수 있다.
`go()` 메서드에서 같은 변수의 값을 변화시켜주고 있다고 가정하면 예기치 않은 상황이 발생할 수 있다.<br>

`go()` 메서드가 실행하고 있을때 `go()`가 호출되는 일이 없어야 한다면 go함수는 원자적으로 수행되어야 하는 부분이다.<br>

이러한 원자적으로 수행되어야 하는 것을 보장해주는 것이 `synchronized` 키워드이다.<br>
`public synchronized void go()` 로 선언해주면 원자적인 수행이 보장되어 진다.


### Javascript에서의 Atomic

정의 -> 메모리가 공유되었을때, 멀티 스레드는 메모리안에 같은 데이터들을 읽거나 쓸 수 있습니다.
Atomic Operations은 예측 가능한 값을 쓰고 읽으며 다음 작업이 시작되기 전에 작업이 완료되고, 작업이 중단되지 않도록 합니다. => 동시성의 오류를 보장해준다는 이야기 인가???

> atomicity is a gurantee of isoliation from interrupts, signals, concurrent process and threads

웹에서 작업을 병렬적으로 실행하는 기본적인 방법은 Web Workers를 사용하는 것이다.
그러나 worker는 각자 분리된 전역 환경에서 실행되기 때문에 worker(또는 메인스레드)간 통신을 통한 간접적인 형태 외에는 데이터가 직접 공유되지 않았다.

```javascript
  // 1024 바이트 크기의 버퍼 생성
  var sab = new SharedArrayBuffer(1024);
  // shared typeArray 객체 생성
  var int32 = new Int32Array(sab);
  // 읽기 쓰레드가 typeArray 객체의 0번 인덱스의 값이 0인지 테스트 한다. true면 sleep 상태에서 대기
  // 대기타임 지정 가능(기본값: 무한대)
  Atomics.wait(int32, 0, 0)

  // 쓰기 스레드가 새로운 값을 저장하면 깨어나 새로운 값을 반환한다.
  console.log(int32[0])
```

Atomics 을 쓸면 sharedArrayBuffer 객체를 사용해야 하는데 모든 브라우저에서 sharedArrayBuffer사용을 보안이슈로 2018년 이후로 금지.
javascript를 사용할때 멀티쓰레드를 사용할지 잘 모르겠다. 

### Race Condition
두개 이상의 프로세스가 공유된 자원을 병행적으로(concurrently) 읽거나 쓰는 동작을 할 때, 공용 데이터에 대한 접근이 어떤 순서에 따라 이루어졌는지에 따라 그 실행결과가 같지 않고 달라지는 상황을 일컬음

a가 먼저 읽었나 b가 먼저 읽었냐에 따라 자원의 상황이 달라지는 것.

두 개의 스레드가 하나의 자원을 놓고 서로 사용하려고 경쟁하려는 상황, 세개의 제어 문제에 직면할 수 있다

* Mutual exclusion(상호 배제)
  * 하나의 프로세스가 공용 데이터를 사용하고 있으면 다른 프로세스가 접근하는 것을 막아야 한다.
* Deadlock (데드락)
  * 상호 배제를 시행했을시에 발생할 수 있는 문제
  * 프로세스가 각자 프로그램을 실행하기 위해 두 자원 모두에 접근해야한다고 가정할 때 프로세스는 두 자원 모두를 필요하므로 두 리소스를 사용하여 프로그램을 수행할 때까지 이미 소유한 리소스를 해제하지 않는다.
  * 프로세스가 두개를 먹어야 끝을 낼수 있는데 한개는 먹고 있고 한개를 더 먹어야 하는 상황이다. 근데 얘는 두개를 먹어야지만 먹고있는 한개를 그만 먹는다. 그래서 먹고있는 한개를 놓지 못한다.(식탐이 많은 친구)
* Starvation (기아상태)
  * 프로세스들이 더 이상 진행을 하지 못하고 계속 블락되어있는 상태, 두 개 이상의 작업이 서로 끝나기만을 기다리고 있다.
  * 한 스레드 혹은 스레드의 그룹이 긴 시간 동안 작업을 수행할 수 없게 된다. 항상 짧은 스레드에게 우선권을 주면 긴 스레드는 계속 작업을 못하게 된다.
<br>
<br>
#### 예방방법

* Semaphore(세마포어)
  * 공유된 자원의 데이터를 여러 프로세스가 접근하는 것을 막는것 
  * 리소스(공유된 자원)의 상태를 나타내는 간단한 카운터
  * 운영체제의 리소스를 경쟁적으로 사용하는 다중 프로세스에서 행동을 조정하거나 동기화 시키는 기술
  * 하나의 스레드만 들어가게 하거나 여러개의 스레드가 들어가게 할수 있다.(이것의 뮤텍스와의 차이)
  * 세마포어 변수 (semWait 연산, semSignal 연산에 대해 알아야함)
  * 세마포어는 정수 값을 가지는 변수로 볼 수 있다. 정수값의 최대 허용치 만큼 사용자(프로세스 or 스레드 겠지?) 접근이 가능

  > sophomore는 2학년, nba 2년차 징크스
* Mutex(뮤텍스)
  * 공유된 자원의 데이터를 여러 스레드가 접근하는 것을 막는 방법
  * Critical Section을 가진 쓰레드들의 런타임이 서로 겹치지 않게 각각 단독으로 실행되게 하는 기술
  * 프로세스 or 스레드가 임계영역에 들어가게 되면 락을 걸어 다른 프로세스 or 스레드 가 접근을 못하게 함
  * 임계영역에서 나오면 lock을 해제


### Semaphore vs Mutex
둘다 Race condition을 예방하기 위해 나온 기술들 
왜 예방해야 하나면 Race condition 상황에서는 deadlock, starvation, mutual exclusion이 발생할 수 있기 때문

임계구역(Critical Section)

각 프로세스에서 공유 데이터를 접근하는 프로그램 코드 부분
한 프로세스가 임계구역을 수행할 때 다른 프로세스가 접근하지 못하도록 해야 한다.

* 세마포어는 공유 자원에 세마포어의 변수만큼의 프로세스(또는 스레드)가 접근 가능
* 뮤텍스는 공유 자원에 1개만의 프로세스(또는 스레드)만 접근 가능
* 현재 수행중인 프로세스가 아닌 다른 프로세스가 세마포어 해제 가능
* 뮤텍스는 lock을 획득한 프로세스가 반드시 그 락을 해제해야 함



<hr>

#### 출처

##### 1. atomic
<https://donxu.tistory.com/entry/%ED%95%A8%EC%88%98%EC%9D%98-%EC%9B%90%EC%9E%90%EC%84%B1atomicity-%EB%B3%B4%EC%9E%A5>

##### 2. atomic in Javascript
<https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Atomics>
<https://www.slideshare.net/barakdrechsler/atomic-javascript>
<https://d2.naver.com/helloworld/7495331>


##### 3. Race condition
<https://iredays.tistory.com/125>


##### 4. Semaphore vs Mutex
<https://junghyun100.github.io/Semaphore&Mutex/>