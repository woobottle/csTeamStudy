# Concurrency 2



## Client/Server Example

```java
ServerSocket serverSocket = new ServerSocket(8009);
while (keepProcessing) { 
  try {
    Socket socket = serverSocket.accept();
    process(socket);
  } catch (Exception e) {
    handle(e); 
  }
}
```

* 서버는 연결을 기다리다가 들어오는 메시지를 처리하고 클라이언트 요청을 기다림

```java
private void connectSendReceive(int i) { 
  try {
    Socket socket = new Socket("localhost", PORT); 
    MessageUtils.sendMessage(socket, Integer.toString(i)); 
    MessageUtils.getMessage(socket);
    socket.close();
  } catch (Exception e) { 
    e.printStackTrace();
  } 
}
```

* 연결하는 클라이언트 코드



```java
@Test(timeout = 10000)
public void shouldRunInUnder10Seconds() throws Exception {
	Thread[] threads = createThreads(); 
  startAllThreadsw(threads); 
  waitForAllThreadsToFinish(threads);
}
```

* 초기화 코드는 생략
* 10_000 밀리초 내에 끝나나 검사,
* 시스템 작업 처리량을 검증하는 전형적인 예
* 클라이언트 요청을 10초 내에 처리해야한다.
* 테스트가 실패하면 어떻게 속도를 올리지? - 단일스레드에서는 노답일듯
* 흠 일단 먼저 어디서 시간을 소모하는지 확인하자
  * I/O 소켓 사용, 데이터베이스 연결, 가상 메모리 스와핑 기다리기 등
  * 프로세서 - 수치 계산, 정규 표현식 처리, 가비지 컬렉션
* 주로 프로세서 연산에 시간을 보내면 새로운 하드웨어를 추가해서 테스트를 통과...
* 어차피 연산에 시간을 보내는 프로그램은 스레드 늘인다고 빨라지지 않음 CPU 사이클은 한계가 있기 때문
* I/O연산에 시간을 보내면? 동시성은 성능을 높여주기도 함, 시스템 한쪽이 I/O를 기다리는 동안 다른 쪽이 뭔가 처리해서 노는 CPU를 효과적으로 활용 가능

### 스레드 추가하기

```java
void process(final Socket socket) { 
  if (socket == null)
		return;
		Runnable clientHandler = new Runnable() { 
      public void run() {
        try {
          String message = MessageUtils.getMessage(socket); 
          MessageUtils.sendMessage(socket, "Processed: " + message); 
          closeIgnoringException(socket);
		    } catch (Exception e) { 
          e.printStackTrace();
		    } 
      }
    };
    Thread clientConnection = new Thread(clientHandler);
	  clientConnection.start(); 
}
```

### Server Observations 서버 살펴보기

* 새 서버가 만드는 스레드 수는 몇 개일까? 
  * 코드에서 한계를 명시하지 않으므로 JVM이 허용하는 수 까지 가능함
* 대다수 간단한 시스템은 괜찮, 하지만 공용 네트워크에 수많은 사용자를 지원하는 시스템이라면? 한번에 몰린다면?
* 그 외의 관점에서,,, 깨끗한 코드와 구조라는 관점에서도 문제가 있음
* 서버 코드가 지는 책임이 몇 개?
  * 소켓 연결 관리
  * 클라이언트 처리
  * 스레드 정책
  * 서버종료 정책
* 다 process함수가 지고있다.
* 추상화 수준도 다양하다.
* 함수가 작긴하지만 분할할 필요가 있다.

```java
public void run() {
  while (keepProcessing) {
    try {
      ClientConnection clientConnection = connectionManager.awaitClient(); 
      ClientRequestProcessor requestProcessor = new ClientRequestProcessor(clientConnection); 
      clientScheduler.schedule(requestProcessor);
    } catch (Exception e) {
      e.printStackTrace(); 
    }
  } 
  connectionManager.shutdown();
}
```

* 스레드 관련 코드는 `ClientScheduler` 라는 클래스에서, 동시성 문제 생기면 여기만 보면 됨

```java
public class ThreadPerRequestScheduler implements ClientScheduler { 
  public void schedule(final ClientRequestProcessor requestProcessor) {
		Runnable runnable = new Runnable() { 
      public void run() {
			requestProcessor.process(); 
      }
		};
		Thread thread = new Thread(runnable);
		thread.start(); 
  }
}
```

* 동시성 정책은 구현하기 쉬움,

* 스레드 관리를 한 곳으로 몰았으니 스레드를 제어하는 동시성 정책도 바꾸기 쉬워진다.

* ex) Java 5 Executor 프레임워크로 옮기려면, 새 클래스를 작성해 대체하면 그만이다.

* ```java
  import java.util.concurrent.Executor; import java.util.concurrent.Executors;
  public class ExecutorClientScheduler implements ClientScheduler { 
    Executor executor;
  	public ExecutorClientScheduler(int availableThreads) { 
      executor = Executors.newFixedThreadPool(availableThreads);
  	}
  	public void schedule(final ClientRequestProcessor requestProcessor) { 
      Runnable runnable = new Runnable() {
  		public void run() { 
         requestProcessor.process();
  		} 
     };
  		executor.execute(runnable); 
    }
  }
  ```

### 결론

* 동시성은 그 자체가 복잡한 문제이므로 단일 책임 원칙이 중요하다.

## Possible Paths of Execution

```java
public class IdGenerator {
	int lastIdUsed;
	public int incrementValue() { 
    return ++lastIdUsed;
	} 
}
```

* 오버 플로는 무시한다.
* 스레드 하나가 IdGenerator 인스턴스를 하나 사용한다고 가정한다.
* 그럼 실행 경로는 단 하나임, 가능한 결과도 단 하나임
* 반환값은 lastIdUsed 값과 동일함, 메서드를 호출하기 전보다 1이 더 큼
* 만약 인스턴스는 그대로인데 스레드는 두개라면? ..

### 경로 수

* 컴파일러가 ++lastIdUsed 를 바이트 코드 명령어 8개로 만들어냄,

* 명령 N개를 스레드 T개가 실행하면 가능한 경로 수는 

* $$
   \frac{(NT)!}{N!^T} 
  $$

* ```java
  public synchronized void incrementValue() { 
    ++lastIdUsed;
  }
  
  ```

* 로 변경하면 경로수가 2개!

### Digging Deeper

* 원자적 연산? - 중단 불가능한거, 스레드에 안뺏기고 한번에 하는거임

* int에 할당하는 연산은 아토믹한데, long에 할당하는건 또 아토믹하지 않음, 64비트-> 32비트씩 나눠서 할당함

* ```java
  public class Example { 
    int lastId;
  	public void resetId() { 
      value = 0;
  	}
  	public int getNextId() { 
      ++value;
  	}
  }
  ```

* 

* 전처리 증가 연산자는 아토믹하지 않음

  * 프레임
    * 프레임은 반환 주소, 메서드로 넘어온 매개변수, 메서드가 정의하는 지역변수를 포함함,
    * 프레임은 호출 스텍을 정의할 때 사용하는 표준 기법
  * 지역 변수
    * 메서드 범위 내에 정의되는 모든 변수
    * 정적 메서드를 제외한 모든 메서드는 기본적으로 this라는 지역변수를 가짐
  * 피연산자 스택
    * JVM이 지원하는 명령 대다수는 매개변수를 받는다.
    * 이런 매개변수를 저장하는 장소임 - LIFO구조

![image](https://user-images.githubusercontent.com/72075148/137786414-f983d8e6-4278-45bc-b42c-5bfe7f86f1b7.png)

* resetId() 함수의 바이트 코드

* 각 명령 사이에 다른 스레드가 끼어들어도 PUTFIELD 명령이 사용하는 정보, 상수 0과 this는 다른 스레드가 못 건드림

* 따라서 연산은 원자적이다.

* long으로 바꿔도 마찬가지임.

* 하지만 getNextId ++연산이 문제임

* ![image](https://user-images.githubusercontent.com/72075148/137786952-7301a94a-0146-43b3-a7f3-0fb6cda2ca3a.png)

  

  * GETFIELD까지 하고, 중단된다면?
  * 둘째 스레드가 lastId를 하나 증가해 43을 얻어가고 , 다시 실행 재개하면 걔는 42을 갖고있었으니.. 43을 반환해버림~

### 결론

* 공유 객체/값이 있는 곳
* 동시 읽기/수정 문제를 일이킬 소지가 있는 코드
* 동시성 문제를 방지하는 방법

## Knowing Your Library

* Synchronized 키워드는 언제나 락 거는거 - 이거 거슬렸긴함
* 같은 값으로 접근을 하는게 아니더라도 무조건 락을 거니가 대가가 비싸죠.
* CAS 연산을 지원함 - AtomicInteger, AtomicReference 등 여러 클래스 ..
  * 메서드가 공유 변수를 갱신하려 하면 현재 변수가 최종적으로 알려진 값인지 확인, 그렇다면 변수 값을 갱신
  * 아니라면 다른 스레드가 끼어들었다는 것 이므로 변수 값을 갱신하지 않음
  * 값을 변경하려면 메서드는 값이 변경되지 않았다는 사실을 확인하고 다시 시도

### 다중 스레드 환경에서 안전하지 않은 클래스

* 디비 연결
* hashTable.containsKeys -> 언제 스레드가 끼어들어 테이블에 값을 추가할 지 모름
* 등등 .. 

## Dependencies Between Methods Can Break Concurrent Code

```java
public class IntegerIterator implements Iterator<Integer> 
  private Integer nextValue = 0;
  public synchronized boolean hasNext() { 
    return nextValue < 100000;
  }
	public synchronized Integer next() {
		if (nextValue == 100000)
		throw new IteratorPastEndException();
		return nextValue++; 
  }
	public synchronized Integer getNextValue() { 
    return nextValue;
	} 
}

IntegerIterator iterator = new IntegerIterator(); 
while(iterator.hasNext()) {
  int nextValue = iterator.next();
	// do something with nextValue
}
```

* 스레드가 IntegerIterator 인스턴스 하나를 공유하게 된다면..?
* 스레드는 적당히 저 정수 목록을 공유하면서 그 값을 처리하고, 목록이 바닥나면 멈춘다.
* 하지만 맨 끝에 두 스레드가 서로를 간섭해 한 스레드가 끝을 지나치는 바람에 예외가 발생할 가능성이 작게나마 ㅂ존재
* 끝에서 hasNext()가 true였고, 끼어들기당해서 또 true 그 이후 뒤 늦게 false로 변경
* 이런 버그는 찾기 어렵다.. 오랜 시간이 지나야 발견되기도하거
* 해결 방안은?
  * 실패를 용인한다.
  * 클라이언트를 바꿔 문제를 해결  / 클라이언트기반 잠금 메커니즘을 구현
  * 서버를 바꿔문제를 해결한다 - 서버에 맞춰 클라도 바꿈 / 서버 기반 잠금 메커니즘을 구현

### 실패를 용인한다.

* 때로 실패해도 괜찮도록 프로그램을 조정해도 됨, 예외를 받아서 처리해도 된다. 조잡하지만 .. 

### 클라이언트-기반 잠금

* 모든 클라이언트 코드를 다음처럼 변경

* ```java
  IntegerIterator iterator = new IntegerIterator();
  while (true) { 
    int nextValue;
    synchronized (iterator) { 
      if (!iterator.hasNext())
  			break;
  		nextValue = iterator.next();
  	}
  	doSometingWith(nextValue); 
  }
  ```

* DRY를 위반하지만 다중 스레드 환경에 안전함

### 서버-기반 잠금

* 아래처럼 하면 클라이언트에서 중복해서 락 걸 필요가 없어짐

* ```java
  public class IntegerIteratorServerLocked { 
    private Integer nextValue = 0;
  	public synchronized Integer getNextOrNull() {
      if (nextValue < 100000) 
        return nextValue++;
  		else
  			return null;
  	} 
  }
  ```

* ```java
  while (true) {
  	Integer nextValue = iterator.getNextOrNull(); 
    if (next == null)
  		break;
  	// do something with nextValue
  }
  ```

* 클라이언트 기반 잠금 매커니즘은 클라이언트가 각자 알아서 서버를 잠궈야하므로 .. 중복 코드가 많다.

* 성능이 더 좋음, - 단일 스레드환경으로 시스템을 배치할 경우 서버만 교체하면 오버헤드가 줄어든다.

* 스레드 정책이 하나다. - 각 클라가 정책을 구현...

* 공유 변수 범위가 줄어든다 .. 클라가 몰라 공유변수를 , 방식도 몰ㄹ..

서버 코드에 손을 못대면? 

```java
public class ThreadSafeIntegerIterator {
	private IntegerIterator iterator = new IntegerIterator();
	public synchronized Integer getNextOrNull() { 
    if(iterator.hasNext())
			return iterator.next(); 
    return null;
	} 
}
```

## 작업 처리량 늘리기

```java

public class PageReader { //...
  public String getPageFor(String url) { 
    HttpMethod method = new GetMethod(url);
  try {
    httpClient.executeMethod(method);
    String response = method.getResponseBodyAsString(); 
    return response;
    } catch (Exception e) { 
    handle(e);
    } finally { 
    method.releaseConnection();
    } 
  }
}
public class PageIterator {
  private PageReader reader; 
  private URLIterator urls;
  public PageIterator(PageReader reader, URLIterator urls) { 
    this.urls = urls;
	  this.reader = reader;
  }
  public synchronized String getNextPageOrNull() { 
    if (urls.hasNext())
	  	getPageFor(urls.next()); 
    else
		  return null; 
  }
  public String getPageFor(String url) { 
    return reader.getPageFor(url);
  } 
}
```



* PageIterator 인스턴스는 여러 스레드가 공유, synchronized 블록이 아주 작게만, 

* 뭐 무튼 .....
* 페이지 읽어오는 시간 I/O 1초
* 분석 처리시간 0.5초
* 라고 하면 ? I/O기다리는동안 다른 스레드가 처리할수있으니 무..

## DeadLock

* 로컬 임시 데이터베이스 연결 풀
* 중앙 저장소 MQ 연결 풀

생성 - 중앙 저장소 연결을 확보한 후 임시 데이터베이스 연결을 얻는다. 중앙 저장소와 통신한 후 임시 데이터베이스에 작업을 저장

갱신 - 임시 데이터베이스 연결을 확보한 후 중앙 저장소 연결을 얻는다. 임시 데이터베이스에서 작업을 읽어 중앙 저장소로 보낸다.

* 풀 크기보다 사용자가 많다면?
* 10명이 생성을 시도해 연결 10개를 확보, 모든 스레드가 연결을 확보한 후 데이터베이스 연결을 확보 전에 중단된다.
* 10명이 갱신을 시도해 데이터베이스 연결 10개를 몯 ㅜ확보, 모든 스레드가 데이터베이스 연결을 확보한 후 중앙 저장소 연결을 확보하기전에 중단된다.
* 생성 스레드 10개는 데이터베이스 연결을 확보하려 기다리고, 갱신 스레드는 중앙 저장소 연결을 확보하려 기다린다..
* 데드락

데드락 조건

* 상호 배제 mutual exclusion
  * 여러 스레드가 한 자원을 공유하나 그 자원은 여러 스레드가 동시에 못쓰고, 개수가 제한적
* 잠금 & 대기 Lock & Wait
  * 스레드가 자원을 점유하면 나머지 필요한 자원까지 모두 점유해 작엄을 마칠떄까지 안내놓음
* 선점 불가 No Preemption
  * 다른 스레드로부터 자원을 뺏지 못함
* 순환 대기 Circular Wait
  * 순환~알지?

### 상호 배제 조건 깨기

* 동시에 사용해도 괜찮은 자원을 사용 - AtomicInteger
* 스레드 수 이상으로 자원을 늘린다 - 이건 오바
* 자원을 점유하기 전 필요한 자원이 모두 있는지 확인한다 - 이거도 ..필요한 자원을 모두 미리 알기 힘듦

### 잠금 & 대기 조건 깨기

* 대기하지 않으면 발생 안함
* 점유 못하면 그냥 다 내놔버리기
* Starvation 문제
* LiveLock - 계속 잠금 단계 진입하느라 점유했다가 내놨다 반복  단순한 CPU 스케쥴링 알고리즘에서 쉽게ㅐ 발생

### 선점 불가 조건 깨기

* 다른 스레드로부터 자원 뺏어오는 방법
* 소유한 스레드에게 풀어달라 요청한다.
* 요청 관리가 어려움..

### 순환 대기 조건 깨기

* 자원을 점유하는..? 스레드의 순서를 ....
* 자원을 할당하는 순서랑 자원을 사용하는 순서가 다를수도 있지? - 필요 이상으로 오랫동안 점유하게 되어버림
* 순서에따라 자원을 할당하기 어렵다ㅡ, 첫 자원 사용하고 나서야 두번째 자원에대한 정보를 얻으면 ..

## 다중 스레드 코드 테스트

* 테스트를 백만번 돌려야 한번 케이스 발생했다..
* 몬테 카를로 테스트 -> 조율 가능하게 유연한 테스트를 만든다... 임의로 값을 조율하면서 테스트서버에서 반복해서 계속 돌린다.
  * 실패 조건은 신중하게 기록한다.

## 스레드 코드 테스트를 도와주는 도구..

* IBM의 ConTest라는 도구 
* 

