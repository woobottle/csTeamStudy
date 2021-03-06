# Chapter.8 Boundaries

- 시스템에 들어가는 모든 소프트웨어를 직접 개발하는 경우는 드물기 때문에
어떤 식으로든 외부 코드를 우리 코드에 깔끔하게 통합해야만 한다.

## 외부 코드 사용하기

- 제공자 → 적용성을 최대한 넓히려 애쓴다.
- 사용자 → 자신의 요구에 집중하는 인터페이스를 바란다.

```jsx
public class Sensors {
	private Map sensors = new HashMap();

	public Sensor getById(String id) {
		return (Sensor) sensors.get(id);
	}
	...
}
```

- 경계 인터페이스인 Map을 Sensors 안으로 숨긴다. 따라서 Map 인터페이스가 변하더라도 나머지 프로그램에는 영향을 미치지 않는다.
- Sensors 클래스는 프로그램에 필요한 인터페이스만 제공한다.
⇒ 이해하기는 쉽지만 오용하기는 어렵다.
⇒ 설계 규칙과 비즈니스 규칙을 따르도록 강제할 수 있다.

- 위와 같은 캡슐화가 목적이 아닌 Map을 여기저기 넘기지 말라는 말.
⇒ 이를 이용하는 클래스나 크래스 계열 밖으로 노출되지 않도록 주의한다.

## 경계 살피고 익히기

- 외부 코드를 익히거나 통합하는 것은 어렵다.
- 그렇기에 곧바로 우리쪽 코드를 작성해 외부 코드를 호출하는 대신 먼저 간단한 테스트 케이스를 작성해 외부 코드를 익히자. (학습 테스트)
    - 학습 테스트는 프로그램에서 사용하려는 방식대로 외부 API를 호출한다.

## 학습 테스트는 공짜 이상이다.

- 학습 테스트는 패키지가 예상대로 도는지 검증한다.
- 일단 통합한 이후라고 해도 패키지가 우리 코드와 호환되리라는 보장은 없다.
- 새 버전이 우리 코드와 호환되지 않으면 학습 테스트가 이 사실을 곧바로 밝혀낸다.
- 패키지의 새 버전으로 이전하기 쉬워지고 낡은 버전을 필요 이상으로 오랫동안 사용하려는 유혹에 빠지기 쉽다.

## 아직 존재하지 않는 코드 사용하기.

- 때로는 우리 지식이 경계 너머 미치지 못하는 코드 영역도 있다. 알려고 해도 알 수가 없다.

![Untitled](Chapter%208%20Boundaries%2015dede2a09a4488e859e5f518cc2cd9b/Untitled.png)

- ADAPTER 패턴으로 API를 사용을 캡슐화해 API가 바뀔 때 수정할 코드를 한 곳으로 모았다.

    [디자인패턴 - 어댑터 패턴 (adapter pattern)](https://jusungpark.tistory.com/22)

## 깨끗한 경계

- 경계에 위치하는 코드는 깔끔히 분리해야한다. 또한 기대치를 정의하는 테스트 케이스도 작성한다.
- 이쪽에선 외부 패키지를 세세하게 알 필요가 없는 대신 통제가 가능한 우리 코드에 의존하는 편이 훨씬 좋다

- 외부 패키지를 호출하는 코드를 가능한 줄여 경계를 관리하자.
- 새로운 클래스로 감싸거나 ADAPTER 패턴을 사용해 우리가 원하는 인터페이스를 패키지가 제공하는 인터페이스로 변환하자.

    ⇒ !?!!?!!?

- 가독성이 높아지며, 경계 인터페이스를 사용하는 일관성도 높아지며, 외부 패키지가 변했을 때 변경할 코드도 줄어든다.