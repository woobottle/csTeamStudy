# Chapter.5 Formatting

## 형식을 맞추는 목적

- 코드 형식은 매우매우 중요하므로 융통성 없이 맹목적으로 따르면 안 된다.
- 코드 형식은 의사소통의 일환이며, 이는 전문 개발자의 일차적인 의무다.

## 적절한 행 길이를 유지하라

- 500줄을 넘지 않고 대부분 200줄 정도인 파일로도 커다란 시스템을 구축할 수 있다.
- 반드시 지킬 엄격한 규칙은 아니지만 바람직한 규칙으로 삼으면 좋겠다.

### 신문 기사처럼 작성하라

- 이름만 보고도 올바른 모듈을 살펴보고 있는지 아닌지를 판단할 정도로 신경 써서 짓는다.
- 첫 부분은 고차원 개념과 알고리즘을 설명한다.
- 아래로 내려갈수록 의도를 세세하게 묘사한다.
- 마지막에는 가장 저차원 함수와 세부 내역이 나온다.

### 개념은 빈 행으로 분리하라

- 빈 행은 새로운 개념을 시작한다는 시각적 단서다.

### 세로 밀집도

- 세로 밀집도는 연관성을 의미한다.
- 밀접한 코드 행은 세로로 가까이 놓여야 한다는 뜻이다.

### 수직 거리

- 서로 밀접한 개념은 한 파일에 속해야 마땅하다. 이게 바로 protected 변수를 피해야 하는 이유 중 하나다.
- 같은 파일에 속할 정도로 밀접한 두 개념은 세로 거리로 연관성을 표현한다.
    - 변수 선언
        
        ⇒ 사용하는 위치에 최대한 가까이 선언한다.
        
        ⇒ 지역 변수는 각 함수 맨 처음에 선언한다.
        
    - 인스턴스 변수
        
        ⇒ 클래스 맨 처음에 선언한다.
        
        (많은 클래스 메서드가 이를 사용하기 때문)
        
        ⇒ 변수 간에 세로로 거리를 두지 않는다.
        
    - 종속 함수
        
        ⇒ 한 함수가 다른 함수를 호출한다면 세로로 가까이 배치한다.
        
        ⇒ 가능하다면 호출하는 함수를 호출되는 함수보다 먼저 배치한다.
        
    - 개념적 유사성
        
        ⇒ 비슷한 동작을 수행하는 일군의 함수도 "개념적 친화도"가 높기 때문에 가까이 배치한다.
        

### 세로 순서

- 신문 기사와 마찬가지로 가장 중요한 개념을 가장 먼저 표현한다.
- 이때는 세세한 사항을 최대한 배제한다.

## 가로 형식 맞추기

- 100자나 120자에 달해도 나쁘지 않다. 하지만 그 이상을 솔직히 주의부족이다.

### 가로 공백과 밀집도

- 가로로는 공백을 사용해 밀접한 개념과 느슨한 개념을 표현한다.

```java
private void measureLine(String line){
	lineCount++;
	int lineSize = link.length();
	...
}
```

- 공백을 넣으면 두 가지 주요 요소가 확실히 나뉜다.
- 함수와 인수는 서로 밀접하기 때문에 공백을 넣지 않았다.

```java
...
return (-b + Math.sqrt(determinant)) / (2*a);
...
```

- 곱셈은 우선순위가 가장 높기 때문에 공백이 없다.
- 항 사이에는 공백이 들어간다.
- 덧셈과 뺄셈은 우선순위가 곱셈보다 낮기 때문.
- 불행히도, 코드 형식을 자동으로 맞춰주는 도구는 대다수가 연산자 우선순위를 고려하지 못하므로 없어지는 경우가 흔하다.

### 가로 정렬

```java
...
this.context =       context;
socket =             s;
...
```

- 위와 같은 정렬은 엉뚱한 부분을 강조해 진짜 의도가 가려지기 때문에 별로 좋지 못하다.
- 정렬이 필요할 정도로 길다면 문제는 목록 "길이"지, 정렬 부족이 아니다.

### 들여쓰기

- 파일 전체에 적용되는 정보가 있고,
파일 내 개별 클래스에 적용되는 정보가 있고,
클래스 내 각 메서드에 적용되는 정보가 있고,
블록 내 블록에 재귀적으로 적용되는 정보가 있다.
이렇듯 Scope로 이뤄진 계층을 표현하기 위해 우리는 코드를 들여쓴다.

- 들여쓰기 무시하기
    - 한 행에 범위를 뭉뚱그린 코드를 피한다.
    
    ```java
    public class CommentWidget ...
    {
    	...
    }
    
    public class CommentWidget ... {
    	...
    }
    ```
    

## 팀 규칙

- 각자 선호하는 규칙이 있을지라도 팀에 속한다면 자신이 선호해야 할 규칙은 바로 팀 규칙이다.
- 좋은 소프트웨어 시스템은 읽기 쉬운 문서로 이뤄진다는 사실을 기억하기 바란다.
- 스타일은 일관적이고 매끄러워야 한다.

## 밥 어저씨의 형식 규칙

- 문서 코드 참조