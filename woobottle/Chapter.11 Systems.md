# 11. System

### 도시를 세운다면?
도시가 돌아가는 이유는 적절한 추상화와 모듈화 때문이다.
큰 그림을 이해하지 못할지라도 각자가 각자의 역할을 이해하고 이를 이행하고 있다.
=> 높은 추상화 수준, 시스템 수준에서 코드의 깨끗함을 유지하는 법을 알려주겠다

### 시스템 제작과 시스템 사용을 분리하라.
소프트웨어 시스템은 준비 과정과 런타임 로직을 분리해야 한다.

```java
  public Service getService() {
    if (service == null) {
      service = new MyServiceImpl(....) // 모든 상황에 적합한 기본 값??
    }
    return service;
  }
```

=> getService는 MyServiceImpl과 생성자 인수에 의존하고 있다.
런타임에서 사용하지 않고 있더라고 의존성이 해결이 안되면 컴파일이 안된다.

### Main 분리
시스템 생성과 시스템 사용을 분리
생성과 관련한 코드는 모두 main 쪽으로, 나머지는 객체 생성, 의존성이 연결되었다고 가정

질문 : dev / production 으로 분리하는 것과는 별개인 것일까??? 

### 팩토리
팩토리 패턴 이란?? => 조건에 따른 객체 생성을 팩토리 클래스로 위임, 팩토리 클래스에서 객체를 생성하는 패턴 (프레임워크 같은 개념?)
추상 팩토리 패턴 이란?? => 연관된 객체들을 묶어서 팩토리 클래스로 생성, 이 팩토리 들을 조건에 따라 생성하도록 다시 팩토리를 만들어서 객체를 생성하는 패턴 (프레임워크를 생성하는 프레임워크 같은 개념???? framework7 cli같은 느낌?) <sup>[[0]](#0-팩토리-패턴)</sup>

추상 팩토리 패턴을 사용, 객체를 생성하는 코드를 어플리 케이션이 모르게 한다.

### 의존성 주입
제어역전 이란 => 
  한 객체가 맡은 보조 책임을 새로운 객체에게 전적으로 넘긴다,
  할리우드 법칙 (에이전시가 모델들의 이력서를 가지고 있고 모델들이 필요할때만 부르겠다.)
  ex) gui 프레임워크에서 프로그램에 요청이 들어오면 이를 처리한다. 주도권이 gui에 있다. 내 프로그램에 있는 것이 아니다. <sup>[[1]](#1-제어역전)</sup>

의존성 주입이란 => MovieLister가 능동적으로 자신이 사용할 객체의 클래스를 생성했다는 것이 문제다.
이것을 Ioc 아이디어를 빌려와서 사용할 객체의 생성을 다른 객체에게 맡겨보자. 그리고 자신에게 객체를 넘겨달라고 하자.<sup>[[2]](#2-의존성-주입)</sup>

![image](https://user-images.githubusercontent.com/50283326/134754914-281cc01c-1b43-480d-afe5-da2128025ea3.png)

아래는 개선된 상황

![image](https://user-images.githubusercontent.com/50283326/134754931-83a017d4-cf57-4404-ad56-f0c64f61a8f3.png)
Assembler은 CSVMovieFinder를 생성하는 객체.
Assembler가 객체를 생성하고 MovieLister에 주입한다. 
이제 Assembler가 다른 MovieFinder(ex. DBMovieFinder)를 생성해서 주입하더라도 이상은 발생하지 않는다.
Spring에서 setter를 이용

```java
// 문제 있던 코드
public interface MovieFinder {
  List findAll();
}

class MovieLister {
  private MovieFinder finder;
  public MovieLister() {
    finder = new CSVMovieFinder("movies1.txt");
  }
  public Movie[] moviesDirectedBy(String arg) {
    List allMovies = finder.findAll();
    for (iterator it = allMovies.iterator(); it.hasNext()) {
      Movie movie = (Movie) it.next();
      if (!movie.getDirecor().equals(arg)) it.remove();
    }
    return (Movie[]) allMovies.toArray(new Movie[allMovies.size()])
  }
}

// 개선한 코드
class MovieLister {
  private MovieFinder finder;
  ...
  public void setFinder(MovieFiner finder) {
    this.finder = finder;
  }
  ...
}
```


=> 제어 역전 기법을 의존성 관리에 적용한 메커니즘이다. 

```java
  // 호출하는 객체는 의존성을 능동적으로 해결한다.
  MyService myService = (MyService)(jndiContext.lookup('NameOfMyService'));
```
클래스가 의존성을 해결하려 시도 하지 않는다. 클래스는 수동적이다.
대신 의존성을 주입하는 방법으로 setter 메서드나 생성자 인수를 제공한다.


### 확장
처음부터 올바르게 시스템을 만들 수 있따는 믿음은 미신이다. 
오늘 주어진 사용자 스토리에 맞춰 시스템을 구현해야 한다. => agile?

<small>소프트웨어 시스템은 물리적인 시스템과 다르다. 관심사를 적절히 분리해 관리한다면 소프트웨어 아키텍처는 점진적으로 발전할 수 있다.</small>

### 횡단 관심사
=> AOP를 사용하여라

영속성과 같은 관심사는 애플리케이션의 자연스러운 객체 경계를 넘나드는 경향이 있다.
**모든 객체가 전반적으로 동일한 방식을 이용하게 만들어야 한다**(ex. 특정 DBMS나 독자적인 파일을 사용하고, 테이블과 열은 같은 명명관례를 따른다, 트랜잭션 의미는 일관적이어야 한다.)

* 이론적으로는 독립된 형태로 구분될 수 있지만 실제로는 코드에 산재하기 쉬운 부분(transaction, authorization, loggin등)

AOP(Aspect-Oriented Programming)은 횡단 관심사에 대해 모듈성을 확보하는 일반적인 방법론 <sup>[[3]](#3-AOP)</sup>
=> 공통 모듈(보안 인증, 로깅 등)을 만든 후에 코드 밖에서 이 모듈을 비즈니스 로직에 삽입하는 것
   기능을 비즈니스 로직과 공통 모듈로 구분하고, 핵심 로직에 영향을 미치지 않고 사이사이에 공통 모듈을 효과적을 잘 끼워넣도록 하는 개발


## 횡단 관심사를 해결하기 위한 세 가지 방법

### 자바 프록시
=> 네트워크에서의 프록시가 아닌 자바에서의 프록시
=> 프록시 패턴이란? <sup>[[4]](#4-자바-프록시)</sup>
  실제 액션을 취하는 객체를 대신한 대리자 역할, 프록시 단계에서 권한을 부여 수 있고 필요에 따라 객체를 생성하거나 사용하기 때문에 메모리 절약 가능
  자신이 보호하는 객체에 대한 액세스 권한을 제어하는것

=> 네트워크에서의 프록시 서버는?<sup>[[5]](#5-네트워크-프록시)</sup>
  서버와 클라이언트 사이에서 대리로 통신을 해주는 서버, 대리로 통신을 수행해주는 것을 프록시 라고 함, 위의 프록시 패턴에서도 프록시라는 개념은 다 같은듯
  드라이브 스루의 직원 같은 개념. 클라이언트는 서버가 어디에 위치해 있는지 모른다
  리버스 프록시는 서버는 클라이언트가 어디에 위치해 있는지 모른다

  캐시 데이터를 사용하기 위해 사용한다.
  보안 목적으로 사용한다.(프록시 방화벽)
  접속 우회 (한국에서 접속이 안되는 사이트들의 경우 ip를 검사해서 한국이면 접속 안되게 막는다. 이때 프록시 서버를 사용해서 다른 나라에서 접속한 것처럼 속일 수 있다.)

```java
// Bank.java (패키지 이름을 감춘다)
import java.util.*;

// 은행 추상화
public interface Bank {
  Collection<Account> getAccounts();
  void setAccounts(Collection<Account> accounts);
}

// BankImpl.java
import java.util.*;

// 추상화를 위한 POJO("Plain Old Java Object") 구현
public class BankImpl implements Bank {
  private List<Account> accounts;

  public Collection<Account> getAccounts() {
    return accounts;
  }

  public void setAccounts(Collection<Account> accounts) {
    this.accounts = new ArrayList<Account>();
    for (Account account : accounts) {
      this.accounts.add(account);
    }
  }
}

// BankProxyHandler.java
import java.lang.reflect.*;
import java.util.*;

// 프록시 API가 필요한 "InvocationHandler"
public class BankProxyHandler implements InvocationHandler {
  private Bank bank;

  public BankProxyHandler (Bank bank) {
    this.bank = bank;
  }

  // InvocationHandler에 정의된 메서드
  public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
    String methodName = method.getName();
    if (methodName.equals("getAccounts")) {
      bank.setAccounts(getAccountsFromDatabase());
      return bank.getAccounts();
    } else if (methodName.equals("setAccounts")) {
      bank.setAccounts((Collection<Account>) args[0]);
      setAccountsToDatabase(bank.getAccounts());
      return null;
    } else {
      ...
    }
  }

  // 세부사항은 여기에 이어진다
  protected Collection<Account> getAccountsFromDatbase() { ... }
  protected void setAccountsToDatabase(Collectdion<Account> accounts) { ... }
}

// 다른 곳에 위치하는 코드
Bank bank = (Bank) Proxy.newProxyInstance(
  Bank.class.getClasLoader(),
  new Class[] { Bank.class },
  new BankProxyHandler(new BankImp())); 
)
```

1. Java Proxy API를 위한 Bank 인터페이스를 작성
2. 추상화를 위한 BankImpl를 구현 -> POJO("Plain Old Java Object")를 구현
3. invocationHandler를 구현하는 BankProxyHandler를 작성
4. BankImpl 객체를 전달, 프록시된 인터페이스를 사용해 모델과 로직이 분리된 코드를 작성할 수 있다.


### 순수 자바 AOP 프레임워크
스프링은 비즈니스 논리를 POJO로 구현한다. 

EJB(Enterprise Java Beans) 등들이 나옴, 이해가 안가서 정리를 못함

### AspectJ 관점

### 테스트 주도 시스템 아키텍처 구축
* 아주 단순하면서도 멋지게 분리된 아키텍처로 소프트웨어 프로젝트를 진행해 결과물을 재빨리 출시한 후, 
기반 구조를 추가하며 조금씩 확장해 나가도 괜찮다.
* 프로젝트를 시작할때는 일반적인 범위, 목표, 일정은 물론이고 결과로 내놓을 시스템의 일반적인 구조도 생각해야 한다. 환경에 대처해 진로를 변경할 능력도 반드시 유지해야 한다.

### 의사 결정을 최적화 하라
최대한 정보를 모아 최선의 결정을 내려야 한다. 너무 일찍 결정하면 고객 피드백을 더 모으고, 프로젝트를 더 고민하고, 구현 방안을 더 탐험할 기회가 사라진다.

### 명백한 가치가 있을 때 표준을 현명하게 사용하라
EJB는 단지 표준이라는 이유로 체택이 되었었다. 가볍고 간단한 설계로 가능했을 프로젝트도 단순히 표준이라는 이유로 EJB를 체택하였었다.
고객의 가치에 따라 움직여야 한다.
> 표준을 사용하면 아이디어와 컴포넌트를 재사용하기 쉽고, 적절한 경험을 가진 사람을 구하기 쉬우며, 좋은 아이디어를 캡슐화 하기 쉽고, 컴포넌트를 엮기 쉽다.
> 하지만 때로는 표준을 만드는 시간이 너무 오래 걸려 업계가 기다리지 못한다. 어떤 표준은 원래 표준을 제정한 목적을 잊어버리기도 한다.

### 시스템은 도메인 특화 언어가 필요하다.
=> 간단한 스크립트 언어나 표준 언어로 구현한 API를 가리킨다. 좋은 DSL(Domain Specific Language)은 도메인 개념과 그 개념을 구현한 코드 사이에 존재하는 의사소통 간극을 줄여준다.
> 도메인 특화언어를 사용하면 고차원 정책에서 저차원 세부사항에 이르기까지 모든 추상화 수준과 모든 도메인을 POJO로 표현할 수 있다.

### 결론
시스템은 깨끗해야 한다.
설계는 가장 단순한 수단을 사용해야 한다.

<hr>

##### 0. 팩토리 패턴
<https://victorydntmd.tistory.com/300>

##### 1. 제어역전 
<https://greatkim91.tistory.com/entry/Dependency-Injection-2>

##### 2. 의존성 주입
<https://greatkim91.tistory.com/entry/Dependency-Injection-2>

##### 3. AOP
<https://isstory83.tistory.com/90>

##### 4. 자바 프록시
<https://blog.seotory.com/post/2017/09/java-proxy-pattern>


##### 5. 네트워크 프록시
<https://liveyourit.tistory.com/251>