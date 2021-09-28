# Systems

* 적절한 추상화와 모듈화, 큰 그림을 몰라도 구성요소는 효율적으로 돌아가게

## Separate Constructing a System from using It

* Construction과 Use는 아주 다르다.

* 소프트웨어 시스템은 애플리케이션 객체를 제작하고, 의존성을 서로 연결하는 준비 과정과 - 런타임 로직을 분리해야한다.

* 시작 단계는 concern, separation of concerns이 가장 오래되고 중요한 설계 기법

* ```java
  public Service getService() { 
  	if (service == null)
  		service = new MyServiceImpl(...); // Good enough default for most cases? return service;
  }
  ```

* Lazy Initialization / Lazy Evaluation 이라는 기법

* 실제 필요할 때까지 생성하지 않으므로 불필요한 부하가 걸리지 않는다. 시작하는 시간이 빨라짐

* 어떤 경우에도 null 포인터를 반환하지 않는다.

* 하지만 getService 메서드가 MyServiceImpl과 생성자 인수(생략되어있음)에 명시적으로 의존한다.

* 런타임 로직에서 MyServiceImpl 객체를 전혀 사용하지 않더라도, 의존성을 해결하지 않으면 컴파일이 안된다.

  * 흠?

* 테스트도 문제, MyServiceImpl이 무거운 객체라면 단위 테스트에서 메서드 호출 전에 테스트 전용 객체를 할당해야함

* 런타임 로직에 객체 생성 로직을 섞어놓은 탓에 모든 실행 경로도 테스트해야한다. - Null / not null 등

* 작게나마 SRP깸

* 실행 논리와 설정 논리는 분리해야 모듈성ㅇ ㅣ높아진다.

* 의존성을 해소하기 위한 방식, 즉 전반적이며 일관적인 방식도 필요하다

### Separation of main

* 생성 관련 코드는 main / main호출하는 모듈로 옮기고 나머지는 모두 객체가 생성 되었고 의존성 연결 된거로 가정
* ![image](https://user-images.githubusercontent.com/72075148/134938455-f3af0044-7d8d-4d3b-b7e0-ca733e0858be.png)

* 모든 화살표가 main에서 애플리케이션 쪽, 애플리케이션은 main이나 객체 생성 과정을 전혀 모른다.



## Factories

* 객체 생성 시점을 애플리케이션이 결정할 필요도 있다.
* 주문 시스템에서 LineItem 인스턴스를 생성해 Order에 추가한다.
* Abstract factory 패턴을 사용한다. Gang of Four
* ![image](https://user-images.githubusercontent.com/72075148/134939458-cf63d17e-e66f-4bf7-9121-88ab62f255aa.png)
* 생성하는 시점은 애플리케이션이 정함
* 생성하는 코드는 모른다.
* 여기서도 Main -> application
* OrderProcessing은 LineItem 생성의 구체적인 방법을 모르고, 팩토리가 알고있음
* 그래도 생성되는 시점을 통제하고, 인수로도 넘길수있다

## Dependency Injection

* 사용과 제작을 분리하는 강력한 메커니즘 하나가 의존성 주입
* 제어 역전 Inversion of Control ( IoC )  기법을 의존성 관리에 적용한 메커니즘
* 제어 역전에서는 한 객체가 맡은 보조 책임을 새로운 객체에게 전적으로 떠넘긴다.
* 새 객체는 SRP, 넘겨 받은 책임만 맡음
* 객체는 의존성 자체를 인스턴스로 만드는 책임은 지지 않음, 대신 전담 메커니즘에 넘겨야함
* 초기 설정은 시스템 전체에서 필요하므로 대개 책임질 메커니즘으로 main 루틴이나 특수 컨테이너 사용
* `MyService myService = (MyService)(jndiContext.lookup(“NameOfMyService”));`
* 호출하는 객체는 실제로 반환되는 객체의 유형을 제어하지 않는다.
* 대신 의존성을 능동적으로 해결한다.
* 클래스가 의존성을 해결하려 시도하지 않는다. 클래스는 수동적
* 대신 의존성을 주입하는 방법으로 setter나 생성자 인수를 제공한다.
* DI 컨테이너는 필요한 객체의 인스턴스를 만든 후 저거로 설정함
* 실제 생성되는 객체 유형은 설정파일이나 특수 생성 모듈에서 코드로 명시,
* 스프링은 XML에서 정의, 이름으로 특정한 객체를 요청
* 초기화 지연으로 얻는 장점을 포기해야하나? 
  * 대다수 DI컨테이너는 팩토리 호출이나 프록시 생성방법을 제공함, 유사하게 구현 가능
  * 흠.

## Scaling Up

* 처음부터 올바르게 시스템을 만들 수 있다는 믿음은 미신이다.

* 반복적이고 점진적인 애자일 방식, 테스트 주도개발, 리펙터링, 

* 깨끗한 코드는 코드 수준에서 시스템을 조정하고 확장하기 쉽게 만든다.

* 하지만 시스템 수준에서는? 시스템 아키텍처는 사전 계획이 필요하지 않을까??..

* ```java
  //11-1
  // An EJB2 local interface for a Bank EJB
  package com.example.banking; 
  import java.util.Collections; 
  import javax.ejb.*;
  public interface BankLocal extends java.ejb.EJBLocalObject { 
    String getStreetAddr1() throws EJBException;
  	String getStreetAddr2() throws EJBException;
  	String getCity() throws EJBException;
  	String getState() throws EJBException;
  	String getZipCode() throws EJBException;
  	void setStreetAddr1(String street1) throws EJBException; 
    void setStreetAddr2(String street2) throws EJBException; 
    void setCity(String city) throws EJBException;
  	void setState(String state) throws EJBException;
    void setZipCode(String zip) throws EJBException; 
    Collection getAccounts() throws EJBException;
  	void setAccounts(Collection accounts) throws EJBException; 
    void addAccount(AccountDTO accountDTO) throws EJBException;
  }
  ```

* Bank 주소, 은행이 소유하는 계좌

* 각 계좌는 Account EJB로 처리한다.

* ```java
  //11-2
  //The corresponding EJB2 Entity Bean Implementation
  package com.example.banking; 
  import java.util.Collections; 
  import javax.ejb.*;
  public abstract class Bank implements javax.ejb.EntityBean { 
    // Business logic...
    public abstract String getStreetAddr1();
    public abstract String getStreetAddr2();
    public abstract String getCity();
    public abstract String getState();
    public abstract String getZipCode();
    public abstract void setStreetAddr1(String
    public abstract void setStreetAddr2(String
    public abstract void setCity(String city);
    public abstract void setState(String state);
    public abstract void setZipCode(String zip);
    public abstract Collection getAccounts();
  	public abstract void setAccounts(Collection accounts); 
  	public void addAccount(AccountDTO accountDTO) {
      InitialContext context = new InitialContext();
  		AccountHomeLocal accountHome = context.lookup("AccountHomeLocal"); 
      AccountLocal account = accountHome.create(accountDTO);
  		Collection accounts = getAccounts();
  		accounts.add(account);
  	}
    // EJB container logic
    public abstract void setId(Integer id);	
    public abstract Integer getId();
    public Integer ejbCreate(Integer id) { ... }
    public void ejbPostCreate(Integer id) { ... }
    // The rest had to be implemented but were usually empty: public void setEntityContext(EntityContext ctx) {} public void unsetEntityContext() {}
    public void ejbActivate() {}
    public void ejbPassivate() {}
    public void ejbLoad() {}
    public void ejbStore() {}
    public void ejbRemove() {}
  }
  ```

* EntityBean은 영속적으로 저장될 Back클래스에 필요한...머시기

  * 관계형 자료, 즉  테이블 행을 표현하는 객체로 메모리에 상주한다.

* 영구 저장소에서 객체와 관계형 자료가 매핑되는 방식, 원하는 트랜잭션 동작 방식, 보안 제약등이 들어가는 xml을 작성

* 이 비지니스 논리가 EJB2 어플리케이션 컨테이너에 강하게 결합된다.

* 클래스 성생헐 때는 컨테이너에서 파생해야하고, 컨테이너가 요구하는 생명주기 메서드도 제공해야한다.

* 독자적인 단위테스트가 어렵다.

  * 컨테이너를 흉내내거나 아니면 실제 서버에 배치해야함

* 객체지향 뿌리가 흔들린다.

  * 빈은 다른 빈을 상속받지 못한다.
  * EJB2빈은 DTO를 정의한다. DTO는 메서드가 없고 사실상 구조체임
  * 동일한 정보를 저장하는 자료 유형이 두 개라는 것, 그래서 한 객체에서 다른 객체로 자료를 복사하는 반복적인 규격 코드가 필요

## Cross Cutting Concerns

* 트랜잭션, 보안, 일부 영속적인 동작은 소스코드가 아닌 deployment descriptors - 배치기술자? 에서 정의한다

* 영속성과 persistence같은 concern은 객체 경계를 넘나드는 경향이 있다.

  * 모든 객체가 동일한 방식으로 이용해야함
  * DBMS나 독자 파일을 만들고 테이블과 열은 같은 몀몀 컨벤션,
  *  트랜잭션 의미가 일관적이면 바람직하다.

  * 모듈화되고 캡슐화된 방식으로 구상 가능
  * 하지만 온갖 객체로 흩어진다.

* 여기서 cross cutting이라는 용어가 나온다. 

* 영속성 프레임워크 또한 모듈화 할 수 있다.

* 도메인 로직도 모듈화할 수 있다.

* EJB가 영속성, 보안, 트랜잭션을 처리하는 방식은 AOP를 예견? Aspect-Oriented Programming

  * 관점-aspect 이라는 모듈 구성 개념은 특정 concern을 support 하려면 시스템에서 특정 지점들이 동작하는 방식을 일관성 있게 바꿔야한다.
  * 명시는 간결한 선언, 프로그래밍 메커니즘으로
  * ex- 영속성. 저장할 객체와 속성을 선언한 후 책임을 영속성 프레임워크에 위임한다.
    * AOP 프레임워크는 대상 코드에 영향을 미치지 않는 상태로 동작 방식을 변경한다.

## Java Proxies

* JDK 프록시를 사용해 영속성을 지원하는 예제

* 계좌목록 갖고오고 설정하는 메서드만

* 

  ```java
  // 11-3
  // JDK Proxy Example
  // Bank.java (suppressing package names...) 
  import java.utils.*;
  // The abstraction of a bank. 
  public interface Bank {
    Collection<Account> getAccounts();
    void setAccounts(Collection<Account> accounts); 
  }
  // BankImpl.java 
  import java.utils.*;
    // The “Plain Old Java Object” (POJO) implementing the abstraction. 
  public class BankImpl implements Bank {
    private List<Account> accounts;
    public Collection<Account> getAccounts() { 
      return accounts;
    }
    public void setAccounts(Collection<Account> accounts) {
  	  this.accounts = new ArrayList<Account>(); 
      for (Account account: accounts) {
    		this.accounts.add(account); 
      }
  	} 
  }
  
  // BankProxyHandler.java 
  import java.lang.reflect.*; 
  import java.util.*;
  
  // "InvocationHandler" required by the proxy API.
  public class BankProxyHandler implements InvocationHandler {
  	private Bank bank;
  	public BankHandler (Bank bank) { 
      this.bank = bank;
  	}
  	// Method defined in InvocationHandler
  	public Object invoke(Object proxy, Method method, Object[] args)
  		throws Throwable {
      String methodName = method.getName(); 
      if (methodName.equals("getAccounts")) {
  			bank.setAccounts(getAccountsFromDatabase());
  			return bank.getAccounts();
  		} else if (methodName.equals("setAccounts")) {
  			bank.setAccounts((Collection<Account>) args[0]);
        setAccountsToDatabase(bank.getAccounts());
  			return 
      } else {}
  	}
  
  	// Lots of details here:
    protected Collection<Account> getAccountsFromDatabase() { ... }
    protected void setAccountsToDatabase(Collection<Account> accounts) { ... }
  }
  
  // Somewhere else...
  Bank bank = (Bank) Proxy.newProxyInstance( 
    Bank.class.getClassLoader(),
  	new Class[] { Bank.class },
  	new BankProxyHandler(new BankImpl())
  );
  ```

* POJO?

* 흠.. 프록시 API에는 invocationHandler를 넘겨 줘야 한다

* 넘긴 InvocationHanlder가 Bank 메서드를 구현하는 데 사용됨

* handler는 자바 리플렉션 api사용해서 제너릭스 메서드에 상응하는 bankImpl메서드로 매핑한다

* 단순한 예제지만 코드가 많고 복잡하다.

* 그게 단점임, 프록시 쓰면 깨끗한 코드 작성이 어렵다.

* 프록시는 시스템 단위로 실행 지점을 명시하는 메커니즘도 제공하지 않는다.

## AOP 프레임워크

* 대부분의 프록시 코드는 판박이라 도구로 자동화 할 수 있다.

* 스프링은 비지니스 논리를 POJO로 구현한다.

  * 도메인에 초점을 맞춘다.
  * 엔터프라이즈 프레임워크에 의존 X
  * 따라서 테스트가 개념적으로 더 쉽고 간단한다.
  * 단순해서 사용자 스토리를 올바로 구현하기 쉽고 뭐어쩌구좋다.

* 설정파일이나 API를 사용해 필수적인 기반 구조를 구현

* 영속성 트랜잭션 보안 캐시 장애조치 같은 횡단 관심사 포함

* 프레임워크는 사용자 모르게 프록시나 바이트코드 라이브러리로 구현함

* 이런 선언들이 요청에 따라 객체를 생성하고 서로 연겨하는 등 DI 컨테이너의 구체적인 동작을 제어

* ```xml
  <beans> ...
  	<bean id="appDataSource" 
          class="org.apache.commons.dbcp.BasicDataSource" 
          destroy-method="close" 
          p:driverClassName="com.mysql.jdbc.Driver" 
          p:url="jdbc:mysql://localhost:3306/mydb" 
          p:username="me"
          />
  	<bean id="bankDataAccessObject" 
          class="com.example.banking.persistence.BankDataAccessObject" 
          p:dataSource-ref="appDataSource"
          />
  <bean id="bank"
  			class="com.example.banking.model.Bank" 
        p:dataAccessObject-ref="bankDataAccessObject"/>
  ... 
  </beans>
  ```

* ![image](https://user-images.githubusercontent.com/72075148/134947171-ccdd6629-e7f2-43f4-8514-408121d4c624.png)

* 클라이언트는 Bank 객체에서 getAccounts()를 호출한다고 믿는다.

* 실제로는 Bank POJO의 기본 동작을 확장한 중첩 decorator 객체 집합으 ㅣ가장 외곽과 통신한다.

* 필요하면 트랜잭션 캐싱 등에도 데코레이터를 추가한다.

* ```java
  XmlBeanFactory bf =
    new XmlBeanFactory(new ClassPathResource("app.xml", getClass()));
  Bank bank = (Bank) bf.getBean("bank");
  ```

  * 애플리케이션이 di컨테이너에 최상휘 객체를 요청하려면
  * 스프링 관련 코드가 없으므로 독립적이다.
  * EJB2 시스템의 강한 결합 문제가 사라짐
  * xml은 장황하고 읽기 어렵다는 문제가 있음에도 명시된 정책이 겉으로 보이진 않지만 자동으로 생성되는 프록시나 관점 논리보다 단순함

```java
package com.example.banking.model; 
import javax.persistence.*; 
import java.util.ArrayList;
import java.util.Collection;

@Entity
@Table(name = "BANKS")
public class Bank implements java.io.Serializable {
  @Id @GeneratedValue(strategy=GenerationType.AUTO) 
  private int id;
  @Embeddable // An object “inlined” in Bank’s DB row 
  public class Address {
  	protected String streetAddr1; 
    protected String streetAddr2; 
    protected String city; 
    protected String state; 
    protected String zipCode;
  }
  
  @Embedded
  private Address address;
  
  @OneToMany(cascade = CascadeType.ALL, fetch = FetchType.EAGER, mappedBy="bank")
  
  private Collection<Account> accounts = new ArrayList<Account>();
  
  public int getId() { 
		return id;
  }
  public void setId(int id) { 
    this.id = id;
  }
  public void addAccount(Account account) { 
    account.setBank(this); 
    accounts.add(account);
  }
  public Collection<Account> getAccounts() { 
    return accounts;
  }
  public void setAccounts(Collection<Account> accounts) { 
    this.accounts = accounts;
	} 
}
```

* 정보다 에너테이션 속에 있으므로 깔끔하다
* 에너테이션에 들어있는 정보는 xml 배치 기술자로 옮겨도 좋다.
* 그럼 진짜 POJO만 남는다.



## AspectJ Aspects

-

## Test Drive the System Architecture

* 코드수준에서 아키텍쳐 관심사를 분리할 수 있다면, 테스트 주도 아키텍쳐 구축이 가능하다.
* 물리적인 구조는 극전인 변경이 어렵다.
* 소프트웨어는 형체가 있긴 하지만 구조가 관점을 효과적으로 분리하면 극적인 변화가 경제적으로 가능하다
* 각기 POJO 객체로 구현되는 모듈화된 관심사 영역으로 구성된다.
* 서로 다른 영역은 해당 영역 코드에 최소한의 영향을 미치는 관점이나 유사한 도구를 사용해 통합한다.
* 이런 구조 역시 테스트 주도 기법에 적용 가능

## Optimize Decision Making

* 명백한 가치가 있을 떄 표준을 현명하게 사용하라
* EJB2는 단지 표준이라는 이유로 많은 팀이 사용함, 과장되게 포장된 표준에 집착하는 바람에 고객 가치가 뒷전으로 밀려난다?



* 표준을 사용하면 아이디어와 컴포넌트를 재사용하기 쉽다
* 적절한 경험을 가진 사람을 구하기 쉬우며
* 좋은 아이디어를 캡슐화하기 쉽고
* 컴포넌트를 엮기 쉽다
* 하지만 때로는 표준을 만드는 시간이 너무 오래 걸려 업계가 기다리지 못한다.
* 어떤 표준은 원래 표준을 제정한 목적을 잊어버리기도 한다.

## Systems Need Domain-Specific Languages

* DSL은 간단한 스크립트언어나 표준 언어로 구현한 API
* 의사소통 간극을 줄여준다.
* 도메인을 잘못 구현할 가능성이 줄어든다.
* 추상화 수준을 코드 관용구나 디자인 패턴 이상으로 끌어올린다.

## 결론

* 추상화 단계에서 의도는 명확히 표현해야한다
* POJO를 작성하고 관점 혹은 관점과 유사한 메커니즘을 활용해 각 구현 관심사를 분리해야한다.
* 

## 







