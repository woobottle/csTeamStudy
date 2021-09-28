# 12. Emergence

### 창발적 설계로 깔끔한 코드를 구현하자

켄트 백이 제시한 단순한 설계규칙 네가지<sub>....쉽지 않다....</sub>

* 모든 테스트를 실행한다
* 중복을 없앤다
* 프로그래머 의도를 표현한다
* 클래스와 메서드 수를 최소로 줄인다.

### 단순한 설계 규칙 1: 모든 테스트를 실행하라
테스트가 가능한 시스템을 만들려고 애쓰면 프로그램의 품질은 좋아진다(결국은 TDD??) => 크기가 작고 목적하나만 수행하는 클래스가 나온다(SRP)
결합도가 높으면 테스트 케이스를 작성하기 어렵다.
테스트 케이스를 많이 작성할수록 개발자는 DIP와 같은 원칙을 적용하고 의존성 주입, 인터페이스, 추상화 등과 같은 도구를 사용해 결합도를 낮춘다. => 설계 품질은 올라간다.

DIP(Dependency Inversion Principle) 의존성 역전 원칙 => 
  * 상위 모듈은 하위 모듈에 의존해서는 안된다.
  * 추상화는 세부 사항에 의존해서는 안된다.
  * **의존 관계를 맺을때 변화하지 않는 것에 의존하라**
  * **확장하기 편하게 공통부분을 묶어서 변화하지 않게 설정**

-> 확장성이 좋아진다. 아래의 코드예시에서 페이 여러종류 이제 막 여러개 추가할 수 있는 것처럼<br>
   객체간의 관계를 최대한 느슨하게 해준다

```java
// 리팩토링 전 코드
package solid.dip;

class SamsungPay {
  String payment() {
    return 'samsung';
  }
}

// 다른 payservice를 만들려 하면 메서드를 매번 추가해주어야 한다.
package solid.dip;

public class PayService {
  private SamsungPay pay;
  
  public void setPay(final SamsungPay pay) {
    this.pay = pay;
  }

  public String payment() {
    return pay.payment();
  }
}

// 리팩토링 후 코드
package solid.dip;

public interface Pay {
  String payment();
}

package solid.dip;

class SamsungPay implements Pay {
  @Override
  public String payment() {
    return 'samsung';
  }
}

class KakaoPay implements Pay {
  @Override
  public String payment() {
    return 'kakao';
  }
}

// 이제 여러개의 pay 추가 쉽게 가능
public class PayService {
  private Pay pay;

  public void setPay(final Pay pay) {
    this.pay = pay;
  }

  public String payment() {
    return pay.payment();
  }
}

// 테스트 코드
package solid.dip;

import org.junit.jupiter.api.Test; 

import static org.assertj.core.api.Assertions.assertThat;

class PayServiceTest {
  private PayService payService = new PayService();

  @Test
  void IsSamsungPayOkay() {
    Pay samsungPay = new SamsungPay();
    payService.setPay(samsungPay);
    assertThat(payService.payment()).isEqualTo("samsung");
  }


  @Test
  void IsKakaoPayOkay() {
    Pay kakaoPay = new KakaoPay();
    payService.setPay(kakaoPay);
    assertThat(payService.payment()).isEqualTo("kakao");
  }
}
```


### 단순한 설계 규칙 2~4: 리팩터링
코드를 점진적으로 리팩터링 해나간다. 
**코드를 정리하면서 시스템이 깨질까 걱정할 필요가 없다. 테스트 케이스가 있으니까**

### 중복을 없애라
비슷한 코드는 더 비슷하게 고쳐주면 리팩터링이 쉬워진다.

```java
int size() {}
boolean isEmpty() {}

// 위에서 따로 구현하지 말고 
// isEmpty 안에서 isSize를 이용하여 코드의 중복을 예방하자
boolean isEmpty() {
  return 0 == size();
}
```

리팩토링 전 코드
```java
public void scaleToOneDimension(float desireDimension, float imageDimension) {
  if (Math.abs(desiredDimension - imageDimension) < errorThreshold) {
    return;
  }
  float scalingFactor = desiredDimension / imageDimension;
  scalingFactor = (float)(Math.floor(scalingFactor * 100) * 0.01f);

  RenderedOp newImage = ImageUtilities.getScaledImage(image, scalingFactor, scalingFactor);
  image.dispose();
  System.gc();
  image = newImage;
}
public synchronized void rotate(int degress) {
  RenderedOp newImage = ImageUtilities.getRotatedImage(image, degrees);
  image.dispose();
  System.gc();
  image = newImage;
}
```

리팩토링 후 코드
```java
public void scaleToOneDimension(float desiredDimension, float imageDimension) {
  if ( Math.abs(desiredDimension - imageDimension) < errorThreshold) {
    return;
  }
  float scalingFactor = desiredDimension / imageDimension;
  scalingFactor = (float)(Math.floor(scalingFactor * 100) * 0.01f);
  replaceImage(ImageUtilities.getScaledImage(image, scalingFactor, scalingFactor));
}

public synchronized void rotate(int degrees) {
  replaceImage(ImageUtilities.getRotatedImage(image, degrees));
}

private void replaceImage(RendereOp newImage) {
  image.dispose();
  System.gc();
  image = newImage;
}
// replaceImage는 SRP를 위반한다.
// image해체 + image 할당도 해서 그런건가? => 왜 SRP를 위반하는 걸까?
// 다른 클래스로 옮겨도 좋겠다.
```

TemplateMethod 패턴 예시
```java
public class VacationPolicy {
  public void accrueUSDDivisionVacation() {
    // 지금까지 근무한 시간을 바탕으로 휴가 일수를 계산하는 코드
    // ...
    // 휴가 일수가 미국 최소 법정 일수를 만족하는지 확인하는 코드
    // ...
    // 휴가 일수를 급여 대장에 적용하는 코드
    // ...
  }
  
  public void accrueEUDivisionVacation() {
    // 지금까지 근무한 시간을 바탕으로 휴가 일수를 계산하는 코드
    // ...
    // 휴가 일수가 유럽연합 최소 법정 일수를 만족하는지 확인하는 코드
    // ...
    // 휴가 일수를 급여 대장에 적용하는 코드
    // ...
  }
}
```

하위 클래스에서 method를 구현하여 각각의 중복되지 않는 정보를 채워준다.
```java
abstract public class VacationPolicy {
  public void accrueVacation() {
    calculateBaseVacationHours();
    alterForLegalMinimums();
    applyToPayroll();
  }

  private void calculateBaseVacationHours() {};
  abstract protected void alterForLegalMinimums();
  private void applyToPayroll() {};
}

public class USVacationPolicy extends VacationPolicy {
  @Override protected void alterForLegalMinimums() {
    // 미국 최소 법정 일수를 사용한다.
  }
}

public class EUVacationPolicy extends VacationPolicy {
  @Override protected void alterForLegalMinimums() {
    // 유럽연합 최소 법정 일수를 사용한다.
  }
}
```

### 표현하라
코드는 개발자의 의도를 분명히 표현해야 한다.
1. 좋은 이름 선택
   1. 이름과 기능이 딴판이여서는 안된다
2. 함수와 클래스 크기를 가능한 줄인다.
   1. 이름 짓기도 쉽고, 구현도 쉽고, 이해도 쉬움
3. 표준 명칭을 사용한다.
   1. 표준 명칭을 사용할 경우 그 이름을 넣어주면 의도를 알기 쉬움
4. 단위 테스트 케이스를 꼼꼼히 작성한다.
   1. 테스트 케이스는 예제가 되기도 하나
   2. 잘 만든 테스트 케이스만 봐도 클래스 기능을 쉽게 이해할 수 있따.


### 클래스와 메서드 수를  최소로 줄여라
클래스와 함수 수를 줄이는 작업도 중요하지만, 테스트 케이스를 만들고 중복을 제거하고 의도를 표현하는 작업이 더 중요하다

### 결론
단순한 설계 규칙을 따른다면 우수한 기법과 원칙을 단번에 활용할 수 있다.


<hr>

##### 1. DIP
<https://huisam.tistory.com/entry/DIP>