# 6. ObjectsAndDataStructure

### 자료 추상화
```java
  // 6-1
  public class Point {
    public double x;
    public double y;
  }
  
  // 6-2
  public interface Point {
    double getX();
    double getY();
    void setCartesian(double x, double y);
    double getR();
    double getTheta();
    void setPolar(double r, double theta);
  }
```

6-2는 직교 좌표계를 사용하는지 극좌표계를 사용하는지 알 길이 없다.
인터페이스는 자료구조를 명백하게 표현한다.
좌표를 읽을때는 각 값을 개별적으로 읽고 설정할때는 두 값을 한꺼번에 설정한다.

6-1은 구현을 노출한다. 변수를 private으로 설정하더라도 
각 값마다 조회 함수와 설정 함수를 제공한다면 구현을 외부로 노출하는 셈

=> 구현을 감추려면 추상화가 필요

클래스의 중요한 의미는 <b>추상 인터페이스를 제공해 사용자가 구현을 모른 채 자료의 핵심을 조작할 수 있어야 진정한 클래스다</b>

```java
  // 구체적인 클래스 -> 구체적인 값으로 제공
  public interface Vehicle {
    double getFuelTankCapacityInGallons();
    double getGallonsOfGasoline();
  }

  // 추상적인 클래스 -> 백분율로 제공
  public interface Vehicle {
    double getPercentFuelRemaining();
  }
```

자료를 세세하게 공개하기 보다는 추상적인 개념으로 표현하는 것이 좋다. => 왜지???
아무 생각 없이 조회/설정 함수를 추가하는 방법이 가장 나쁘다.

### 자료/객체 비대칭
객체는 추상화 뒤로 자료를 숨긴 채 자료를 다루는 함수만 공개한다.
자료구조는 자료를 그대로 공개하며 별다른 함수는 제공하지 않는다.

절차적
```java
  // 6-5
  public class Square {
    public Point topLeft;
    public double side;
  }

  public class Rectangle {
    public Point topLeft;
    public double height;
    public double width;
  }

  public class Circle {
    public Point center;
    public double radius;
  }

  public class Geometry {
    public final double PI = 3.141592;

    public double area(Object shape) throws NoSuchShapeException {
      if (shape instanceof Square) {
        Square s = (Square)shape;
        return s.side * s.side;
      } else if (shape instanceof Rectangle) {
        Rectangle r = (Rectangle)shape;
        return r.height * r.width;
      } else if (shape instanceof Circle) {
        Circle c = (Circle)shape;
        return PI * c.radius * c.radius;
      }
      throw new NoSuchShapeException();
    }
  }
```
=> 도형 추가하면 class 다 변경되어야 한다.

객체 지향적
```java
  // 6-6
  public class Square implements Shape {
    private Point topLeft;
    private double side;

    public double area() {
      return side * side;
    }
  }

  public class Rectangle implements Shape {
    private Point topLeft;
    private double height;
    private double width;

    public double area() {
      return height * width;
    }
  }

  public class Circle implements Shape {
    private Point center;
    private double radius;
    private final double PI = 3.141592;

    public double area() {
      return PI * radius * radius;
    }
  }
```
=> 새 함수를 추가하고자 하면 모든 클래스 변경 하여야 한다.

```java
  // (자료구조를 사용하는) 절차적인 코드는 기존 자료 구조를 변경하지 않으면서 새 함수를 추가하기 쉽다.
  // 반면 객체 지향 코드는 기존 함수를 변경하지 않으면서 새 클래스를 추가하기 쉽다.

  // 절차적인 코드는 새로운 자료 구조를 추가하기 어렵다. 그러려면 모든 함수를 고쳐야 한다.
  // 객체 지향 코드는 새로운 함수를 추가하기 어렵다. 그러려면 모든 클래스를 고쳐야 한다.
```

### 디미터 법칙
디미터 법칙 => 모듈은 자신이 조작하는 객체의 속사정을 몰라야 한다는 법칙이다.
객체의 자료를 숨기는 대신 함수를 공개하자
(객체지향에서 가장 중요한 것은 '객체가 어떤 메세지를 주고 받는가' 이다,  객체가 어떤 데이터를 가지고 있는가가 아니다.)


'클래스 C의 메서드 f는 다음과 같은 객체의 메서드만 호출해야 한다'
* 클래스 C
* f가 생성한 객체
* f 인수로 넘어온 객체
* C 인스턴스 변수에 저장된 객체
  
```java
  // 디미터 법칙을 어기는 코드
  final String outputDir = ctxt.getOptions().getScratchDir().getAbsolutePath();

  // getOptions 함수가 반환하는 객체의 함수를 호출하고 또 반환 객체의 함수를 호출한다.
```

자신이 구현한 것을 너무 잘알기 때문에 그것을 오히려 경계하기 위해 나온 법칙, 결합도가 높아지고 문제를 야기한다.

디미터 법칙의 예시
```java
  // 잘못된 예시
  @Getter // lombok 라이브러리 이고 이걸 사용하면 getEmail(), getName() 등등을 자동으로 선언해준다
  public class User {
    private String email;
    private String name;
    private Address address;
  }

  @Getter
  public class Address {
    private String region;
    private String details;
  }

  @Service
  public class NotificationService {
    public void sendMessageForSeoulUser(final User user) {
      if('서울'.equals(user.getAddress().getRegion())) {
        sendNotification(user);
      }
    }
  }

  // 잘된 예시 
  // 데이터로 사용자의 지역을 파악하는 것이 아니라, 메시지를 보내 서울 지역에 사는지 파악 해보자
  public class Address {
    private String region;
    private String details;

    public boolean isSeoulRegion() { 
      return '서울'.equals(region);
    }
  }

  @Getter
  public class User {
    private String email;
    private String name;
    private Address address;

    public boolean isSeoulUser() {
      return address.isSeoulRegion();
    }
  }

  @Service
  public class NotificationService {
    public void sendMessageForSeoulUser(final User user) {
      if(user.isSeoulUser()) {
        sendNotification(user);
      }
    }
  }

  // 출처 : https://mangkyu.tistory.com/147
```


### 기차 충돌
메서드 체이닝이 너무 길어지면 조잡하게 여겨지는 듯

```java
  Options opts = ctxt.getOptions();
  File scratchDir = opts.getScratchDir();
  final String outputDir = scratchDir.getAbsolutePath();
```

위 예제는 ctxt, Options, ScratchDir 이 객체라면 디미터 법칙을 위반
자료구조라면 당연히 내부 구조를 노출하므로 디미터 법칙이 적용되지 않는다.

자료구조는 무조건 함수 없이 공개 변수만 포함하고 객체는 비공개 변수와 공개 함수를 포함한다면 문제는 간단해진다.
=> 예시 첨부

### 잡종 구조
절반은 객체, 절반은 자료구조인 잡종 구조
단점만 모아놓은 구조임 피하자 요런건

### 구조체 감추기
ctxt, options, scratchDir이 객체라면 위에서처럼 코드를 짜면 안된다 => 객체는 내부구조를 감춰야 한다.

객체에게는 뭔가를 하라고 말해야지 속을 드러내라고 말하면 안된다 => 메소드로 액션을 지정하라는 의미인듯
```java
  // 좋지 못한 예
  ctxt.getAbsolutePathOfScratchDirectoryOption();
  ctxt.getScratchDirectoryOption().getAbsolutePath();

  String outFile = outputDir + "/" + className.replace('.', '/') + ".class";
  FileOutputStream fout = new FileOutputStream(outFile);
  BufferedOutputStream bos = new BufferedOutputStream(fout);


  // 좋은 예
  BufferedOutputStream bos = ctxt.createScratchFileStream(classFileName);
```
ctxt는 내부 구조를 드러내지 않으며, 모듈에서 해당 함수는 자신이 몰라야 하는 여러 객체를 탐색할 필요가 없다.


### 자료 전달 객체
공개 변수만 있고 함수가 없는 클래스, DTO(Data Transafer Object)라 한다.
데이터베이스와 통신하거나 소켓에서 받은 메시지의 구문을 분석할 때 유용하다.

### 활성 레코드 
DTO의 특수한 형태.
공개 변수가 있거나 비공개 변수에 조회/설정 함수가 있는 자료 구조지만, 대개 save나 find와 같은 탐색 함수도 제공한다.
활성레코드는 자료구조로 취급하는것이 좋다.


### 결론
객체는 동작을 공개하고 자료를 숨긴다. 
기존 동작을 변경하지 않으면서 새 객체 타입을 추가하기는 쉽다.
기존 객체에 새 동작을 추가하는 것은 어렵다.

자료구조는 자료를 노출한다.
기존 자료구조에 새 동작을 추가하기는 쉽다.
기존 함수에 새 자료구조를 추가하기는 어렵다.

새로운 자료 타입을 추가해야 한다 => 객체가 적합
새로운 동작을 추가하는 것이 많다 => 자료구조 & 절차적인 코드가 적합(객체 방식으로 하면 모든 객체에 일일히 추가해야함 => 상속으로 조져도 되긴 하지만 그래도 결국 재구현 해야한다)