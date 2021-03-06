# Chapter.6 ObjectsAndDataStructures

- 변수를 비공개로 정의하는 이유가 있다. 남들이 변수에 의존하지 않게 만들고 싶어서다.
충동이든 변덕이든, 변수 타입이나 구현을 마음대로 바꾸고 싶어서다.

- 변수 사이에 함수라는 계층을 넣는다고 구현이 저절로 감춰지지 않는다.
구현을 감추려면 추상화가 필요하다.
- 추상 인터페이스를 제공해 사용자가 구현을 모른 채 자료의 핵심을 조작할 수 있어야 진정한 의미의 클래스다

- 자료를 세세하게 공개하기보다는 추상적인 개념으로 표햔하는 편이 좋다.
개발자는 객체가 포함하는 자료를 표현할 가장 좋은 방법을 심각하게 고민해야 한다.

## 자료/객체 비대칭

- 객체와 자료 구조 사이에 벌어진 차이를 보여준다.
객체는 추샇와 뒤로 자료를 숨긴 채 자료를 다루는 함수만 공개한다.
자료 구조는 자료를 그대로 공개하며 별다른 함수를 제공하지 않는다.
이 개념은 사실상 정반대다.
- 절차적인 코드는 새로운 자료 구조를 추가하기 어렵다. 그러려면 모든 함수를 고쳐야 한다. (객체 지향 기법)
객체 지향 코드는 새로운 함수를 추가하기 어렵다. 그러려면 모든 클래스를 고쳐야 한다. (자료 구조)

## 디미터 법칙

- 모듈은 자신이 조작하는 객체의 속사정을 몰라야 한다는 법칙 (휴리스틱 - 간편추론의 방법)
- 객체는 자료를 숨기고 함수를 공개한다.
⇒ 조회 함수로 내부 구조를 공개하면 안 된다는 의미.

### 기차 충돌

```jsx
final String outputDir = ctxt.getOptions().getScratchDir().getAbsolutePath();
```

- 일반적으로 조잡하다 여겨지는 방식이므로 피하는 편이 좋다.

```jsx
Options opts = ctxt.getOptions();
File scratchDir = opts.getScratchDir();
final String outputDir = scratchDir.getAbsolutePath();
```

- 위 함수는 ctxt 객체가 Options를 포함하며, Options가 ScratchDir을 포함하며, ScratchDir이 AbsolutePath를 포함한다는 사실을 안다.
- 함수 하나가 아는 지식이 굉장히 많다.
- 위 코드를 사용하는 함수는 많은 객체를 탐색할 줄 안다는 말.
- 위 예제가 디미터 법칙을 위반하는지 여부는 ctxt, Options, ScratchDir이 객체인지 아니면 자료 구조인지에 달렸다.
- 객체 → 디미터 법칙 위반
- 자료 구조 → 디미터 법칙 적용 X

```jsx
final Stringi outputDir = ctxt.options.scratchDir.absolutePath;
```

- 조회 함수를 사용하는 바람에 혼란을 일으켰지만 위와 같이 구현했다면 디미터 법칙을 거론할 필요가 없어진다.

### 잡종 구조

- 절만은 객체, 절만은 자료 구조인 구조.
- 새로운 함수는 물론이고 새로운 자료 구조도 추가하기 어렵다. (단점만 모아놓은 구조)

### 구조체 감추기

- 만약 ctxt, options, scratchDir이 진짜 객체라면 위 코드처럼 줄줄이 엮어서는 안 된다. (객체라면 내부 구조를 감춰야 하기 때문)
- ctxt가 객체라면 뭔가를 하라고 말해야지, 속을 드러내라고 말하면 안 된다.
- 무엇을 위해 코드가 사용되는지 파악 후 그 액션을 직접 취하도록.

    ```jsx
    BufferedOutputStream bos = ctxt.createScratchFileStream(classFileName);
    ```

- ctxt는 내부 구조를 드러내지 않으며. 모듈에서 해당 함수는 자신이 몰라야 하는 여러 객체를 탐색할 필요가 없다.

## 자료 전달 객체

- 자료 구조체의 전형적인 형태는 공개 변수만 있고 함수가 없는 클래스다.
⇒ 이런 구조체를 자료 전달 객체(Data Transfer Object, DTO)라 한다.
- 데이터베이스와 통신하거나 소켓에서 받은 메시지의 구문을 분석할 때 유용하다.
- 일반적인 형태는 Bean 구조다.
    - 비공개 변수를 조회/설정 함수로 조작한다.
    - 별다른 이익을 제공하지 않는다.

    ### 활성 레코드

    - DTO의 특수한 형태다.
    - 공개 변수가 있거나 비공개 변수에 조회/설정 함수가 있는 자료 구조지만, 대개 save나 find와 같은 탐색 함수도 제공한다.
    - 데이터베이스 테이블이나 다른 소스에서 자료를 직접 변환한 결과다.
    - But, 비즈니스 규칙 메소드를 추가해 객체로 취급하는 것은 바람직하지 않다.
    자료 구조도 아니고 객체도 아닌 잡종 구조가 나오기 때문.
    - 해당 구조는 자료 구조로 취급하고 비즈니스 규칙을 담으면서 내부 자료를 숨기는 객체는 따로 생성한다.

## 결론

- 객체
    - 동작을 공개 / 자료를 숨김
    - 기존 동작을 변경하지 않으면서 새 객체 타입을 추가하기는 쉽다.
    - 기존 객체에 새 동작을 추가하기는 어렵다
- 자료 구조
    - 별다른 동작 없이 자료를 노출
    - 기존 자료 구조에 새 동작을 추가하기는 쉽다.
    - 기존 함수에 새 자료 구조를 추가하기는 어렵다.

- 우수한 개발자는 편견없이 이 사실을 이해해 직면한 문제에 최적인 해결책을 선택한다.