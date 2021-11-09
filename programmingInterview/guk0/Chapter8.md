## 재귀 호출

### 이해
- 기본 케이스(base case) : 재귀 호출 중에 자신을 호출하지 않아도 처리할 수 있는 하위 작업.
- 재귀 케이스(recursive case) : 루틴에서 자신을 호출하여 하위 작업을 수행하는 케이스.
``` c
  // 팩토리얼
  n! = n * (n-1)!

  int factorial(int n) {
    if (n > 1) {
      return n * factorial(n-1) // 재귀 케이스
    } else {
      return 1 // 기본 케이스
    }
  }
```

<img src="https://user-images.githubusercontent.com/48615016/140596817-df5323c2-aaf2-4991-bf6c-45b709b0703a.png" width="300">

<br>

- 모든 중간 결과 값까지 반환. 래퍼 함수 활용.
> 복잡한 재귀 호출 루틴의 경우 초기화를 위해 래퍼 함수를 별도로 만드는 것이 좋다.
``` c
int allFactorial(int n) {
  int[] arr = new int[n == 0 ? 1 : n];
  doAllFactorial(n, arr, 0);
  return arr;
}

int doAllFactorial(int n, int[] arr, int level) {
  if (n > 1) {
    arr[level] = n * doAllFactorial(n-1, arr, level + 1);
    return arr[level];
  } else {
    arr[level] = 1;
    return 1;
  }
}

```
<!-- 
``` c
  int factorial(int n, int level) {
    int[] arr = new int[n == 0 ? 1 : n];

    if (n > 1) {
      arr[level] = n * factorial(n-1);
      return arr[level] // 재귀 케이스
    } else {
      return 1 // 기본 케이스
    }
  }

  factorial(3, 0);
``` -->

- 재귀 호출은 매우 강력한 테크닉이지만 루틴 호출에서 오버헤드가 크기 때문에 오버헤드가 없는 반복문을 사용하는 것이 일반적으로 더 좋다.

``` c++
int factorial(int n) {
  int i, val = 1;
  for (i = n, i > 1, i--) {
    val *= i;
  }

  return val
}
```
- 지역 변수는 프로그램의 스택에 할당되기 때문에 루틴이 재귀적으로 호출될 때마다 별도의 지역 변수를 가지게 됨.
- 재귀 호출을 하게 되면 자동적으로 프로그램의 스택에 변수 값이 저장.
- 따라서 직접 스택을 만들고 수동으로 지역 변수 값을 그 스택에 넣고 꺼내면서 재귀호출을 쓰지 않아도 됨.
- 스택을 기반으로 반복형 루틴을 만드는 방법이 같은 루틴을 재귀 호출을 써서 구현하는 것에 비해 훨씬 복잡함.
- 별다른 얘기가 없다면 재귀 알고리즘은 재귀 호출을 써서 구현하는 편이 더 좋다.



## 문제

### 문자열 조합
> 문자열에 있는 문자들의 모든 가능한 조합을 출력하는 함수를 구현하라. 조합의 길이는 1이상이고 문자열 길이 이하이다. 문자의 배치 순서만 다를 뿐
> 같은 문자들이 들어가 있는 조합은 같은 조합으로 간주한다. 즉, '123'이라는 문자열이 입력됐을 때 '12'와 '31'은 서로 다른 조합이지만 '21'은 '12'와 같다.

```java

public class Combinations {
  private StringBuilder out = new StringBuilder();
  private final String in;

  public Combinations( final String str ) {
    in = str;
  }

  public void combine() {
    combine(0);
  }

  private void combine(int start) {
    for (int i = start; i < in.length(); ++i) {
      out.append(in.charAt(i));
      System.out.println(out);
      if (i < in.length()) {
        combine(i + 1);
      }
      out.setLength(out.length() - 1);
    }
  }
}

```

### 전화 단어
> 일곱 자리 전화번호를 입력받아 주어진 수를 표현할 수 있는 모든 가능한 단어 또는 글자 조합을 출력하는 루틴을 작성. 2~9만 글자로 바꿀 수 있음.
> 866-2665

``` java
public class TelephoneNumber {
  private static final int PHONE_NUMBER_LENGTH = 7;
  private final int[] phoneNum;
  private char[] result = new char[PHONE_NUMBER_LENGTH];

  public TelephoneNumber(int[] n) {
    phoneNum = n;
  }

  public void printWords(int curDigit) {
    if (curDigit == PHONE_NUMBER_LENGTH) {
      System.out.println(new String(result));
      return;
    }
    for (int i = 1; i<=3; ++i) {
      result[curDigit] = getCharKey(phoneNum[curDigit], i);
      printWords(curDigit + 1);
      if (phoneNum[curDigit] == 0 || phoneNum[curDigit] == 1) return;
    }
  }
}
```