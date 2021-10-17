# Appendix. Concurrency2.md

### 클라이언트/서버 예제

```java
while (keepProcessing) {
  try {
    Socket socket = serverSocket.accept();
    process(socket);
  } catch (Exception e) {
    handle(e);
  }
}
```

```java
private void connectSendReceive(int i) {
  try {
    Socket socket = new Socket('localhost', PORT);
    MessageUtils.sendMessage(socket, Integer.toString(i));
    MessageUtils.getMessage(socket); socket.close();
  } catch (Exception e) {
    e.printStackTrace();
  }
}
```

테스트케이스
```java
@Test(timeout = 10000)
public void shouldRunInUnder10Seconds() throws Exception {
  Thread[] threads = createThreads();
  startAllThreads(threads);
  waitForAllThreadsToFinish(threads);
}
```

어플리케이션이 어디서 시간을 보내는지 알아야 한다.
* I/O - 소켓사용, 데이터베이스 연결, 가상 메모리 스와핑 기다리기 등에 시간을 보낸다
* 프로세서 - 수치 계산, 정규 표현식 처리, 가비지 컬렉션 등에 시간을 보낸다

I/O 연산에 시간을 보낸다면 동시성이 성능을 높여주기도 한다.   
시스템 한쪽이 I/O를 기다리는 동안에 다른 쪽이 뭔가를 처리해 놓으면 cpu를 효과적으로 활용할 수 있다.

### 스레드 추가하기

서버의 process 함수가 주로 I/O 연산에 시간을 보낸다면, 스레드를 추가하자
```java
void process(final Socket socket) {
  if (socket == null) {
    return;
  }

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


### 서버 살펴보기 
새 서버가 만드는 수레드 수는 몇 개일까? JVM이 허용하는 수까지 가능할 것이다.   
위의 경우 너무 많은 사용자가 한꺼번에 몰린다면 시스템이 동작을 멈출지도 모른다.   

현재 서버 코드가 지는 책임  
* 소켓 연결 관리
* 클라이언트 처리
* 스레드 정책
* 서버 종료 정책 

이 모든 것을 process 함수가 진다. 너무 가혹하다   
서버 프로그램은 SRP를 위반한다.  
다중 스레드 프로그램을 깨끗하게 유지하려면 잘 통제된 몇 곳으로 스레드 관리를 모아야 한다.  

각 책임을 클래스로 분할한 서버 코드
```java
public void run() {
  while (keepProcessing) {
    try {
      ClientConnection clientConnection = connectionManager.awaitClient();
      ClientRequestProcessor requestProcessor = new ClientRequestProcessor(clientConnection);
      clientScheduler.schedule(requestProecessor);
    } catch (Exception e) {
      e.printStackTrace();
    }
  }
  connectionManager.shutDown();
}
```

스레드와 관련한 코드는 모두 ClientScheduler라는 클래스에 존재한다.   
서버에 동시성 문제가 생긴다면 살펴볼 코드는 단 한곳이다.   

```java
public interface ClientScheduler {
  void schedule(ClientRequestProcessor requestProcessor);
}
```

동시성 정책은 구현하기 쉽다
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

### 가능한 실행경로

```java
public class IdGenerator {
  int lastIdUsed;

  public int incrementValue() {
    return ++lastIdUsed;
  }
}
```

만약 IdGenerator 인스턴스는 그대로지만 스레드가 두 개라면? 각 스레드가 incrementValue 메서드를 한 번씩 호출한다면 가능한 결과는 무엇일까? 가능한 실행 경로는? lastIdUsed 초깃값을 93으로 가정할 때 가능한 결과는 다음과 같다.

* 스레드 1이 94를 얻고, 스레드 2가 95를 얻고, lastIdUsed가 95가 된다
* 스레드 1이 95를 얻고, 스레드 2가 94를 얻고, lastIdUsed가 95가 된다
* 스레드 1이 94를 얻고, 스레드 2가 94를 얻고, lastIdUsed가 94가 된다

#### 경로수 

return ++lastIdUsed라는 자바 코드 한 줄은 바이트 코드 명령 8개에 해당한다. 두 스레드가 명령 8개를 뒤섞어 실행할 가능성이 충분하다.

8! / 8^2 = 12870 가지수 가능

```java
public synchronized void incrementValue() {
  ++lastIdUsed;
}
```

`synchronized`를 추가하면 가능한 경로수는 2개로 줄어든다.

#### 결론

바이트 코드를 속속들이 이해할 필요는 없지만 아래의 것들은 알아야 한다.

* 공유 객체/값이 있는 곳
* 동시 읽기/수정 문제를 일으킬 소지가 있는 코드
* 동시성 문제를 방지하는 방법


### 라이브러리를 이해하라
Jvm 내부, java 클래스에서 동시성을 제어할 수 있는 것들에 대한 내용

### 메서드 사이에 존재하는 의존성을 조심하라
```java
public class IntegerIterator implements Iterator<Integer> {
  private Integer nextValue = 0;

  public synchronized boolean hasNext() {
    return nextValue < 100000;
  }
  public synchronized Integer next() {
    if (nextValue == 100000) {
      throw new IteratorPastEndException();
    }
    return nextValue++;
  }
  public synchronized Integer getNextValue() {
    return nextValue;
  }
}
```

```java
IntegerIterator iterator = new IntegerIterator();
while (iterator.hasNext()) {
  int nextValue = iterator.next();
  // nextValue로 뭔가를 한다.
}
```

위의 문제는 경계조건에서 문제가 발생할 가능성이 다분하다(nextValue가 100000일떄)

해결방법 세 가지
* 실패를 용인한다.
* 클라이언트를 바꿔 문제를 해결한다. 즉 클라이언트-기반 잠금 메커니즘을 구현한다.
* 서버를 바꿔 문제를 해결한다. 서버에 맞춰 클라이언트도 바꾼다. 즉, 서버-기반 잠금 메커니즘을 구현한다.

##### 클라이언트-기반 잠금
```java
IntegerIterator iterator = new IntegerIterator();

while (true) {
  int nextValue;

  synchronized(iterator) {
    if (!iterator.hasNext()) {
      break;
    }
    nextValue = iterator.next();
  }
  doSomethingWith(nextValue);
}
```

각 클라이언트는 IntegerIterator 객체에 락을 건다.
사람이 할짓이 아니다.

##### 서버-기반 잠금
서버쪽
```java
public class IntegerIteratorSeverLocked {
  private Integer nextValue = 0;
  public synchronized Integer getNextOrNull() {
    if (nextValue < 100000 ) {
      return nextValue++;
    } else {
      return null;
    }
  }
}
```
클라이언트 쪽
```java
while (true) {
  Integer nextValue = iterator.getNextOrNull();
  if (next == null) {
    break;
  }
  // nextValue로 뭔가를 한다.
}
```

서버-기반 잠금이 일반적으로 더 바람직하다.
1. 코드 중복이 줄어든다.
2. 성능이 좋아진다.(단일 스레드 환경으로 시스템을 배치할경우 서버만 교체하면 오버헤드가 줄어든다)
3. 오류가 발생할 가능성이 줄어든다.
4. 스레드 정책이 하나다.
5. 공유 변수 범위가 줄어든다.


### 작업 처리량 높이기

```java
public class PageReader {
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
```

URL iterator를 받아 목록에 들어있는 페이지 내용을 제공하는 Iterator다
```java
public class PageIterator {
  private PageReader reader;
  private URLIterator urls;

  public PageIterator(PageReader reader, URLIterator urls) {
    this.urls = urls;
    this.reader = reader;
  }

  public synchronized String getNextPageOrNull() {
    if(urls.hasNext()) {
      return getPageFor(urls.next());
    } else {
      return null
    }
  } 

  public String getPageFor(String url) {
    return reader.getPageFor(url);
  }
}
```

PageIterator 인스턴스는 여러 스레드가 공유한다.
synchronized로 감싸진 부분이 작다는 것에 주목

위의 경우 여러 스레드가 처리하면 단일 스레드에 비해 작업 처리량이 좋다.


### 데드락 

다음 네가지 조건을 모두 만족하면 데드락이 발생한다.
* 상호 배제
* 잠금 & 대기
* 선점 불가
* 순환 대기

상호배제   
=> 여러 스레드가 한 자원을 공유하나 그 자원은 
* 여러 스레드가 동시에 사용하지 못하며
* 개수가 제한적이다.

=> 스레드 하나가 자원 먹고 있으면 다른 스레드는 먹지 못함
라면 상호배제 조건 만족

잠금 & 대기 
=> 스레드가 자원을 점유하면 작업을 마칠때 까지 이미 점유한 자원을 내놓지 않는다.

선점 불가
=> 한 스레드가 다른 스레로부터 자원을 빼앗지 못한다. 자원을 점유한 스레드가 스스로 내놓지 않는 이상 다른 스레드는 그 자원을 점유하지 못한다.

순환 대기 
스레드 1이 자원 1을 먹고 있는데 자원 2가 필요하다.   
스레드 2가 자원 2를 먹고 있는데 자원 1이 필요하다.   
죽음의 포옹 이라 불림


##### 상호 배제 조건 깨기
* 동시에 사용해도 괜찮은 자원을 사용한다. AtomicInteger
* 스레드 수 이상으로 자원 수를 늘인다. 
* 자원을 점유하기 전에 필요한 자원이 모두 있는지 확인한다.

##### 잠금 & 대기 조건 깨기
* 대기하지 않으면 데드락이 발생하지 않는다. 각 자원을 점유하기 전 확인한다. 만약 어느 하나라도 점유하지 못한다면 지금까지 점유한 자원을 몽땅 내놓고 처음부터 다시 시작한다.

발생할 수 있는 문제점
* 기아 => 한 스레드가 계속해서 자원을 못먹음
* 라이브락 => 여러 스레드가 한꺼번에 잠금 단계로 진입하는 바람에 계속해서 자원을 점유했다 내놨다를 반복한다.

##### 선점 불가 조건 깨기
* 다른 스레드로부터 자원을 뺏어오자. 필요한 자원이 잠겼다면 자원을 소유한 스레드에게 풀어달라 요청한다.

##### 순환 대기 조건 깨기
* 가장 흔한 전략
* 모든 스레드가 자원을 점유하는 순서를 같게 하고 그 순서로만 자원을 할당한다. => 데드락 불가능 

문제점
1. 자원을 할당하는 순서와 자원을 사용하는 순서가 다를 수 있다. 맨 처음 점유한 자원을 아주 나중에 쓸 수도 있다.
2. 순서에 따라 자원을 할당하기 어렵다.

```java
public class ClassWithThreadingProblem {
  int nextId; 

  public int takeNextId() {
    return nextId++;
  }
}
```

1. nextId의 현재 값을 기억ㅎ나다
2. 스레드 두 개를 생성, 각각 takeNextId()를 한 번씩 호출
3. nextId가 2 증가했는지 확인
4. 2 대신에 1만 증가할 때까지 위 단계를 반복한다.

```java
package example;

import static org.junit.Assert.fail;

import org.junit.Test;

public class ClassWithThreadingProblemTest {
  @Test
  public void twoThreadsShouldFailEventually() throws Exception {
    final ClassWithThreadingProblem classWithThreadingProblem = new ClassWithThreadingProblem();

    Runnable runnable = new Runnable() {
      public void run() {
        classWithThreadingProblem.takeNextId();
      }
    };

    for (int i = 0; i < 50000; ++i) {
      int startingId = classWithThreadingProblem.lastId;
      int expectedResult = 2 + startingId;

      Thread t1 = new Thread(runnable);
      Thread t2 = new Thread(runnable);
      t1.start();
      t2.start();
      t1.join();
      t2.join();

      int endingId = classWithThreadinProblem.lastId;

      if(endingId != expectedResult) {
        return;
      }
    }

    fail('Should have exposed a threading issue but it did not.');
  }
}
```
