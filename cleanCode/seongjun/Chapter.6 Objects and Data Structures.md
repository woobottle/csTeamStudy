

# Objects and Data Structures

* 남들이 변수에 의존하지 않게 만들고 싶어서, private으로 만든다.
* get / set 함수를 public하게 만들어서 private 변수를 외부에 노출하나?

## Data Abstraction

#### Concrete Point

```java
// 6-1
public class Point { 
	public double x; 
  public double y;
}
```

* 직교 좌표계를 사용한다. 개별적으로 좌표값을 읽고 설정하게 강제한다
* 변수를 private으로 했어도 get / set을 제공하면 구현을 외부로 노출
* 변수 사이에 함수 계층을 넣어도 구현이 감춰지지는 않는다. 추상화 해야함

#### Abstract Point

```java
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

*  직교 좌표계인지, 극 좌표계인지 모른다, 둘 다 아닐수도있고, 그럼에도 인터페이스는 자료구조를 명백하게 표현
* 클래스 메서드가 접근 정책을 강제한다. 좌표를 읽을 때는 각 값을 개별적으로 일겅야한다.
* 설정할 때는 두 값을 한꺼번에 설정해야한다.

```java
//6-3 Concrete Vehicle
public interface Vehicle {
	double getFuelTankCapacityInGallons(); 
	double getGallonsOfGasoline();
}
```

* 연료 상태를 구체적인 숫자 값으로 알려준다.
* 변수에서 읽어 온다는 사실이 거의 확실함

```java
//6-4 Abstract Vehicle
public interface Vehicle {
	double getPercentFuelRemaining();
}
```

* 연료 상태를 백분율이라는 추상적인 개념으로 알려준다.
* 정보가 어디서 오는지 전혀 드러나지 않는다.



* 자료를 세세하게 공개하기 보다는 추상적인 개념으로 표현하는 편이 더 좋다.
* 인터페이스나 get/set 함수 만으로는 추상화가 이뤄지지 않는다.



## Data / Object Anti-Symmetry 비대칭

* 객체는 추상화 뒤로 자료를 숨긴 채 자료를 다루는 함수만 공개한다
* 자료구조는 자료를 그대로 공개하며 별다른 함수는 제공하지 않는다.

```java
//6-5 Procedural Shape
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
	public final double PI = 3.141592653589793;
	public double area(Object shape) throws NoSuchShapeException {
		if (shape instanceof Square) { 
      Square s = (Square)shape; 
      return s.side * s.side;
		}
    else if (shape instanceof Rectangle) { 
      Rectangle r = (Rectangle)shape; 
      return r.height * r.width;
		}
		else if (shape instanceof Circle) {
			Circle c = (Circle)shape;
			return PI * c.radius * c.radius; 
    }
		throw new NoSuchShapeException(); 
  }
}
```

* Geometry는 세가지 도형 클래스를 다룸
* 각 도형 클래스는 간단한 자료 구조, 메서드를 제공하지 않는다.
* Geometry에서 동작을 구현함
* 만약 둘레를 구하는 perimeter() 함수 구현을 원한다면 함수 하나만 추가, 클래스는 영향을 받지 않는다.
* 반대로 새 도형을 추가하고싶다면? Geometry에 모든 함수를 고쳐야한다.



```java
// 6-6 Polymorphic Shape
public class Square implements Shape { 
  private Point topLeft;
	private double side;
	public double area() { 
    return side*side;
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
	public final double PI = 3.141592653589793;
	public double area() {
		return PI * radius * radius;
	} 
}
```

* 객체 지향적인 도형 클래스이다. Geometry 클래스는 필요없다.
* area는 다형 메서드임, 새 도형을 추가해도 기존 함수에 아무런 영향 X
* 새 함수를 추가하고 싶으면 도형 클래스를 다 고쳐야함
  * VISITOR / Dual-Patch같이 잘 알려진 기법으로 이 문제를 해결한다.
  * 이 기법도 대가가 따르고, 절차적인 구조를 반환함
  * VISITOR는 주로 상속없이 클래스에 메서드를 효과적으로 추가하기 위해 사용한다. 하지만 합성 객체의 내부 구조가 VISITOR에 열려서 캡슐화를 위반함
* 6-5 / 6-6는 상호 보완적임, 사실상 반대다? 객체와 자료구조는 근본적으로 양분된다...

```
자료구조를 사용하는 절차적인 코드는 기존 자료 구조를 변경하지 않으면서 새 함수를 추가하기 쉽다. 반면 객체지향 코드는 기존 함수를 변경하지 않으면서 새 클래스를 추가하기 쉽다.

절차적인 코드는 새로운 자료구조를 추가하기 어렵다. 그러려면 모든 함수를 고쳐야한다. 객체지향 코드는 새로운 함수를 추가하기 어렵다. 그러려면 모든 클래스를 고쳐야한다.
```

* 모든 것이 객체라는 생각이 미신이다.??
* 때로는 단순한 자료구조와 절차적인 코드가 가장 적합한 상황도 있다.



## The Law of Demeter

* 잘 알려진 휴리스틱으로, 모듈은 자신이 조작하는 객체의 속 사정을 몰라야한다.
* 객체는 자료를 숨기고 함수를 공개한다. 객체는 조회 함수로 내부 구조를 공개하면 안 된다.
* 클래스 C 의 메서드 f는 아래만 호출 해야함
  * 클래스 C
  * f가 생성한 객체
  * f인수로 넘어온 객체
  * C 인스턴스 변수에 저장된 객체

* 허용된 메서드가 반환하는 객체의 메서드는 호출하면 안된다.

* ```java
  final String outputDir = ctxt.getOptions().getScratchDir().getAbsolutePath();
  ```

### Train Wrecks

* 위 같은 코드를 기차 충돌이라고 부른다.

* ```java
  Options opts = ctxt.getOptions();
  File scratchDir = opts.getScratchDir();
  final String outputDir = scratchDir.getAbsolutePath();
  ```

* 이렇게 하는게 차라리 나음

* 이거도 디미터를 위반하나??

* 디미터 - 객체면 내부 구조를 숨겨야하므로 위반한다?

* 디미터 - 자료구조면 당연히 내부 구조를 노출하므로 적용되지 않는다

* 
  
  ```java
  final String outputDir = ctxt.options.scratchDir.absolutePath;
  ```
  
* 자료구조는 함수 없이 퍼블릭 변수만 포함하고, 객체는 private 변수 / public 함수를 포함한다면 간단.

* 하지만 단순 자료구조에도 get / set 정의를 요구하는 프레임 워크나 표준이 있다.

??

### Hybrids

* 반은 객체, 반은 자료구조인 잡종 구조가 나옴
* get / set 함수가 비공개 변수를 그대로 노출해서 사용하고픈 유혹에 빠짐
* 이런 구조는 새 함수, 새 자료구조를 추가하기 어려움

### Hiding Structure

* ctxt, options, scratchDir이 객체라면? - 내부구조를 감춰야하니까... 저리하면 안댐

1. `ctxt.getAbsolutePathOfScratchDirectoryOption()`
   * ctxt 객체에 공개해야 하는 메서드가 너무 많아진다.

2. `ctx.getScratchDirectoryOption().getAbsolutePath()`
   * getScratchDirectoryOption()이 자료구조를 반환한다고 가정한다

```java
String outFile = outputDir + "/" + className.replace('.', '/') + ".class"; 
FileOutputStream fout = new FileOutputStream(outFile); 
BufferedOutputStream bos = new BufferedOutputStream(fout)
```

* 같은 모듈에서 가져온 코드임
* 추상화 수주을 뒤섞어 놓아 다소 불편하다.... 무튼 임시 디렉터리의 절대경로를 얻으려는 이유가, 임시파일을 생성하기 위함

3. `BufferedOutputStream bos = ctxt.createScratchFileStream(classFileName);`

* 내부 구조를 드러내지 않으며, 모듈에서 자신이 몰라야 하는 여러 객체를 탐색할 필요가 없다. 디미터 위반안함

### Data Transfer Objects

* 자료 구조체의 전형적인 형태는 public 변수만 있고 함수가 없음
* DTO라고함 
* 데이터베이스와 통신/ 소켓에서 받은 메시지의 구문을 분석할 때 유용하다.
* 가공되지 않은 정보를 애플리케이션 코드에서 사용할 객체로 변환하는 일련의 단계에서 가장 처음으로 사용하는 구조체
* 좀더 일반적인 형태는 bean 구조다.
  * private 변수를 get / set 함수로 조작한다.
  * 사이비 캡슐화..? 별다른 이익을 제공하지 않는다.

```java
// 6-7 
public class Address { 
  private String street; 
  private String streetExtra; 
  private String city; 
  private String state; 
  private String zip;
	public Address(String street, String streetExtra, 
                 String city, String state, String zip) {
		this.street = street; this.streetExtra = streetExtra; this.city = city;
		this.state = state;
		this.zip = zip;
	}
	public String getStreet() { 
    return street;
	}
	public String getStreetExtra() { 
    return streetExtra;
	}
	public String getCity() { 
    return city;
	}
  
  public String getState() { 
    return state;
	}
	public String getZip() { 
    return zip;
	} 
}  
```

## Active Record

* DTO의 특수한 형태다.
* public 변수가 있거나, private 변수에 get / set 함수가 있는 자료구조.
* 대개 save, find와 같은 탐색 함수도 제공한다.
* 데이터베이스 테이블이나 다른 소스에서 직접 자료를 변환한 결과다.
* 엑레에 비지니스 로직을 추가한 메서드를, 이런 자료구조를 객체 취급하는 것도흔하다.
* 엑레는 자료구조로 취급한다. 비지니스 로직을 담으면서, 내부 자료를 숨기는 객체는 따로 생성한다.

## Conclusion

* 객체는 동작을 공개하고 자료를 숨긴다

* 기존 동작을 변경하지 않으면서 새 객체 타입을 추가하기는 쉬운 반면, 기존 객체에 새 동작을 추가하기는 어렵다.

* 자료구조는 별다른 동작 없이 자료를 노출한다.

* 기존 자료구조에 새 동작을 추가하기는 쉬우나 기존 함수에 새 자료 구조를 추가하기는 어렵다.

* 새 자료 타입을 추가하는 유연성이 필요하면 객체

* 새 동작을 추가하는 유연성이 필요하면 자료구조와 절차적인 코드가 더 적합하다

* ### 편견 없이 이 사실을 이해해 직면한 문제에 최적인 해결책을 선택한다.



