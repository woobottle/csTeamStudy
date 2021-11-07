# 8. 재귀 호출

### 재귀 호출의 이해

정렬이나 검색, 종주 문제에는 간단한 재귀적인 형태의 풀이가 있는 경우가 흔하다.    
재귀 호출을 하다보면 자신을 호출하지 않고도 처리할 수 있는 하위 작업이 나온다.   

> 재귀 호출은 기본 케이스 + 재귀 케이스로 이루어져 있다.

기본 케이스 => 루틴에서 재귀 호출을 하지 않아도 되는 케이스
재귀 케이스 => 루틴에서 자신을 호출하여 하위 작업을 수행하는 케이스   

팩토리얼의 예시
```java
int factorial(int n) {
  if (n > 1) { // 재귀 케이스
    return factorial(n-1) * n;
  } else { // 기본 케이스
    return 1
  }
}
```

> 모든 재귀 케이스는 결국에는 기본 케이스로 넘어가야만 한다.

=> 기본 케이스로 넘어가지 않으면 끝이 안나서 결국엔 스택이 터지니까 그런듯

재귀 호출을 이용할 시에 메모이제이션을 사용하면 더 효율적인 알고리즘을 짤수 있다.
```java
int factorial(int n, int[] results, int level) {
  if (n > 1) {
    if (results[level]) {
      return results[level];
    }
    results[level] = n * factorial(n-1, results, level + 1)
    return results[level];
  } else {
    results[level] = 1;
    return 1
  }
}
```

팩토리얼처럼 단순한 재귀 호출 루틴의 경우에는 상당수의 컴퓨터 아키텍처에서 실제 계산보다는 호출에 따르는 오버헤드 때문에 더 많은 시간을 소모하게 된다.


오버헤드란? 
> 프로그램의 실행흐름 도중에 동떨어진 위치의 코드를 실행시켜야 할 때, 추가적으로 시간, 메모리, 자원이 사용되는 현상    
> 실행흐름이 도중에 끊기고, 함수를 사용하기 위해 스택메모리를 할당, 매개변수가 있다면 대입연산까지도 일어난다.   
> 이때 예상하지 못한 자원들이 소모되는 현상이 바로 오버헤드 현상

반복문을 사용하는 경우 위의 오버헤드가 필요 없기 때문에 일반적으로 더 효율이 좋다.

* 지역 변수는 프로그램의 스택에 할당되기 때문에 루틴이 재귀적으로 호출될 때마다 별도의 지역 변수를 가지게 된다. 
재귀 호출을 하게 되면 자동적으로 프로그램의 스택에 변수 값이 저장된다.


### 재귀 호출 문제

1. 문자열 조합 
> 문자열에 있는 문자들의 모든 가능한 조합을 출력하는 함수를 구현하라. 조합의 길이는 1 이상이고    
> 문자열 길이 이하이다. 문자의 배치 순서만 다를 뿐 같은 문자들이 들어가 있는 조합은 같은 조합으로 간주한다.    
> 즉 '123'이라는 문자열이 입력됐을 때 '12'와 '31'은 서로 다른 조합이지만 '21'은 '12'와 같다.

```
입력 시작 위치부터 입력 문자열 끝까지의 각 글자에 대해
  출력 문자열의 현재 위치에 그 글자를 선택
  글자들을 출력 문자열로 출력
  현재 글자가 입력 문자열의 마지막 글자가 아니면
    방금 선택한 글자 다음 글자에서 반복을 시작하여
    다음 위치부터 시작하는 나머지 조합 생성
  출력 문자열의 마지막 문자 삭제
```

```java
public class Combinations {
  private StringBuilder out = new StringBuilder();
  private final String in;

  public Combinations(final String str) {in = str;}

  public void combine() { combine(0); }
  private void combine(int start) {
    for (int i = start; i < in.length(); i++) {
      out.append(in.chatAt(i));
      System.out.println(out);
      if (i < in.length()) 
        combine(i + 1);
      out.setLength(out.length() - 1)
    }
  } 
}
```

```python
def solution(sentence) :
  listed = sentence
  result = []

  def get_all_list(elements, start) :
    for i in range(start, len(sentence)) :
      print(elements, i)
      elements.append(listed[i])
      result.append("".join(elements[:]))
      if i < len(listed) :
        get_all_list(elements, i + 1)
      elements.pop()
    
  get_all_list([], 0);
  return result


print(solution('wxyz'))
```

2. 전화 단어
어떤 글자가 바뀌면 그 바로 오른쪽에 있는 글자가 모든 가능한 값을 한 번씩 지나가야만 원래 글자가 바뀐다.

```
현재 숫자가 마지막 숫자를 지나버리면
  마지막이므로 단어 출력
그렇지 않으면
  현재 숫자를 나타낼 수 있는 세 글자에 대해
    글자가 현재 자리를 나타내도록 한다.
    다음 자리로 넘어가서 재귀 호출
    현재 자리가 0이나 1이면 반환
```

```java
public class TelephoneNumber {
  private static final int PHONE_NUMBER_LENGTH = 7;
  private final int[] phoneNum;
  private char[] result = new char[PHONE_NUMBER_LENGTH];

  public TelephoneNumber (int[] n) { phoneNum = n; }

  public void printWords(){ printWords(0); }

  private void printWords(int curDigit) {
    if (curDigit == PHONE_NUMBER_LENGTH) {
      System.out.println(new String(result));
      return;
    }
    for (int i = 1; i<= 3; ++i) {
      result[curDigit] = getCharKey(phoneNum[curDigit], i);
      printWords(curDigit + 1);
      if (phoneNum[curDigit] == 0 || phoneNum[curDigit] == 1) return;
    }
  }
}
```