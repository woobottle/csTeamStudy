# Emergence

창발성

* 켄트벡의 설계 규칙
  1. 모든 테스트를 실행한다
  2. 중복을 없앤다.
  3. 프로그래머 의도를 표현한다
  4. 클래스와 메서드 수를 최소로 줄인다.

## Run All The Tests 

* 테스트 케이스를 항상 통과하는 시스템은 - 테스트가 가능한 시스템
* 검증 불가능한 시스템은 출시하면 안된다.
* 테스트 가능한 시스템을 만들려고 애쓰면 설계 품질이 높아진다.
* 크기가 작고 목적 하나만 수행하는 클래스가 나온다.
* SRP를 준수하면 테스트가 쉽고, 테케가 많을수록 개발자는 더 테스트가 쉽게 코드를 작성한다.
* 결합도가 높으면 테케 작성이 어렵다.
* DIP의 원칙을 적용하고, 인터페이스, 추상화 같은 도구를 사용해 결합도를 낮춘다.
* 이 규칙을 따르면 자동으로 낮은 결합도 높은 응집력 가능

### Refactoring

* 테케를 모두 작성했으면 코드와 클래스를 정리해도 괜찮다. 점진적으로 리펙터링한다.
* 코드 추가할 때마다 멈추고 설계를 조감한다.
* 새로 추가하는 코드가 설계 품질을 낮추나?
  * 깔끔하게 정리 후 테스트 돌린다.
* 리펙터링 단계에서는 설계 품질을 높이는 기법이라면 뭐든 적용한다.
  * 응집도를 높이고 
  * 결합도를 낮추고 
  * 관심사를 분리하고 
  * 시스템 관심사를 모듈로 나누고 
  * 함수와 클래스 크기를 줄이고
  * 더 나은 이름을 선택하고

## No Duplication

* 중복은 추가 작업, 추가 위험, 불필요한 복잡도를 뜻한다.

* 비슷한 코드는 더 비슷하게 고치면 리팩터링이 쉬움

* 구현 중복도 중복의 한 형태임

* ```java
  int size() {} 
  boolean isEmpty() {}
  
  // isEmpty에서 size메서드를 사용해서 코드를 중복해 구현할 필요 없어지게
  boolean isEmpty() { 
    return 0 == size();
  }
```java
public void scaleToOneDimension(
  float desiredDimension, float imageDimension) {
  if (Math.abs(desiredDimension - imageDimension) < errorThreshold)
    return;
  
  float scalingFactor = desiredDimension / imageDimension; 
  scalingFactor = (float)(Math.floor(scalingFactor * 100) * 0.01f);
  RenderedOp newImage = ImageUtilities.getScaledImage( image, scalingFactor, scalingFactor);
  image.dispose(); 
  System.gc(); 
  image = newImage;
}
public synchronized void rotate(int degrees) {
  RenderedOp newImage = ImageUtilities.getRotatedImage( image, degrees);
  image.dispose(); 
  System.gc(); 
  image = newImage;
}
```
* 일부가 중복임 

  
  ```java
public void scaleToOneDimension(
		float desiredDimension, float imageDimension) {
  		if (Math.abs(desiredDimension - imageDimension) < errorThreshold) return;
				float scalingFactor = desiredDimension / imageDimension; 
  			scalingFactor = (float)(Math.floor(scalingFactor * 100) * 0.01f);
  		replaceImage(ImageUtilities.getScaledImage( image, scalingFactor, scalingFactor));
}

```java
public synchronized void rotate(int degrees) {
	replaceImage(ImageUtilities.getRotatedImage(image, degrees));
}
private void replaceImage(RenderedOp newImage) { 
  image.dispose();
  System.gc();
  image = newImage;
}
```

*  클래스가 SRP를 위반한다.
* 새로 만든 클래스를 다른 클래스로 옮겨도 좋겠다.

```java
public class VacationPolicy {
  public void accrueUSDivisionVacation() {
    // code to calculate vacation based on hours worked to date // ...
    // code to ensure vacation meets US minimums
    // ...
    // code to apply vaction to payroll record
    // ... 
  }
  public void accrueEUDivisionVacation() {
    // code to calculate vacation based on hours worked to date // ...
    // code to ensure vacation meets EU minimums
    // ...
    // code to apply vaction to payroll record
    // ...
  } 
}
```

* 최소 법정 일수를 계산하는 코드만 제외하면 두개는 거으 ㅣ동일
* 최소 법정 일수를 계산하는 알고리즘은 직원 유형에 따라 살짝 편한다.
* TEMPLATE METHOD 패턴으로 중복을 제거

```java
abstract public class VacationPolicy { 
  public void accrueVacation() {
    calculateBaseVacationHours();
    alterForLegalMinimums();
    applyToPayroll();
    }
	private void calculateBaseVacationHours() { /* ... */ }; 
  abstract protected void alterForLegalMinimums(); 
  private void applyToPayroll() { /* ... */ };
}
public class USVacationPolicy extends VacationPolicy { 
  @Override protected void alterForLegalMinimums() {
		// US specific logic 
  }
}
public class EUVacationPolicy extends VacationPolicy { 
  @Override protected void alterForLegalMinimums() {
		// EU specific logic 
  }
}
```

* 하위클래스는 중복되지 않는 정보만 제공해 accrueVaction 알고리즘에서 빠진 구멍만 메운다.

## Expressive

* 자신이 이해하는 코드를 짜기는 쉽다.

1. 좋은 이름을 선택한다
2. 함수와 클래스 크기를 가능한 줄인다.
3. 표준 명칭을 사용한다.
4. 단위 테스트 케이스를 꼼꼼히 작성한다.

## Minimal Classes and Methods

* 중복을 제거하고 의도 표현하고 SRP를 준수하는 기본 개념을 극단으로 치달으면 득보다 실ㅇ ㅣ많다.
* 가능한 줄이라고 제안한다.
* 무의미하고 독단적인 정책으로 늘어나는 때가 있다.. 가능한 독단적인 견해는 멀리하고 실용적인 방식을 택한다.
* 클래스와 함수를 줄이는 작업도 중요하지만 - 마지막 우선순위임 무튼 테케 만들고 중복 제거하고 의도 표현하는게 더 중요하다.

## Conclusion

* 경험을 대신할 기법이 있나? 없지 여기 기법들은 수십년 노하우니까 ..