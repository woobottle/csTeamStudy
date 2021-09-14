### 형식을 맞추는 목적
코드 형식은 의사소통의 일환이다. 의사소통은 전문 개발자의 일차적인 의무다

### 적절한 행 길이를 유지하라
200줄이 넘지 않는 많은 개수의 파일로도 대규모의 프로젝트를 만들 수 있다.

### 신문 기사처럼 작성하라
이름은 간단하면서도 설명이 가능하게 짓는다.
소스 파일 첫 부분은 고차원 개념과 알고리즘을 설명한다. 아래로 내려갈수록 의도를 세세하게 묘사한다.
마지막에는 가장 저차원 함수와 세부 내역이 나온다.

### 개념은 빈 행으로 분리하라.
빈 행은 문단의 개념

### 세로 밀집도
세로 밀집도는 연관성을 의미. 
서로 밀접한 코드 행은 세로로 가까이 놓여야 한다.

### 수직 거리
서로 밀접한 개념은 세로로 가까이 둬야 한다. 
물론 두 개념이 서로 다른 파일에 속한다면 규칙이 통하지 않는다.
하지만 타당한 근거가 없다면 서로 밀접한 개념은 한 파일에 속해야 마땅하다.
이게 바로 protected 변수를 피해야 하는 이유 중 하나다.

### 변수 선언

### 인스턴스 변수
인스턴스 변수는 클래스 맨 처음에 선언한다. => 나도 맨 위에 선언하는 것을 선호한다

### 종속 함수
한 함수가 다른 함수를 호출한다면 두 함수는 세로로 가까이 배치한다. 
또한 가능하다면 호출하는 함수를 호출되는 함수보다 먼저 배치한다.

### 개념적 유사성
```java
  public class Assert {
    static public void assertTrue(String message, boolean condition) {
      if (!condition) {
        fail(message);
      }
    }

    static public void assertTrue(boolean condition) {
      assertTrue(null, condition);
    }

    static public void assertFalse(String message, boolean condition) {
      assertTrue(message, !condition);
    }

    static public void assertFalse(boolean condition) {
      assertFalse(null, condition);
    }
  }
```

### 세로 순서

### 가로 형식 맞추기
100자 120자 까지 ㄱㅊ

### 가로 공백과 밀집도
```java
  private void measureLine(String line) {
    lineCount++;
    int lineSize = line.length();
    totalChars += lineSize;
    lineWidthHistogram.addLine(lineSize, lineCount);
    recordWidthestLine(lineSize);
  }
```

함수와 인자 사이에는 공백을 주지 않는다.
할당 연산자를 강조하려고 앞뒤에 공백을 줬다.

곱셈끼리는 공백없이 더하기,빼기 같은경우는 공백 있이
수식의 우선순위를 공백으로 표시한다.

### 가로 정렬

### 들여쓰기
들여쓰기는 너무 중요하지!!

### 들여쓰기 무시하기

### 가짜 범위