# JUnit Internals



* JUnit 프레임워크에서 가져온 코드 평가하기



### ComparisionCompactorTest.jsva
```java
package junit.tests.framework;
import junit.framework.ComparisonCompactor; 
import junit.framework.TestCase;
public class ComparisonCompactorTest extends TestCase {
  public void testMessage() {
    String failure= new ComparisonCompactor(0, "b", "c").compact("a"); 
    assertTrue("a expected:<[b]> but was:<[c]>".equals(failure));
  }

  public void testStartSame() {
    String failure= new ComparisonCompactor(1, "ba", "bc").compact(null); 
    assertEquals("expected:<b[a]> but was:<b[c]>", failure);
  }

  public void testEndSame() {
    String failure= new ComparisonCompactor(1, "ab", "cb").compact(null); 
    assertEquals("expected:<[a]b> but was:<[c]b>", failure);
  }

  public void testSame() {
    String failure= new ComparisonCompactor(1, "ab", "ab").compact(null); 
    assertEquals("expected:<ab> but was:<ab>", failure);
  }

  public void testNoContextStartAndEndSame() {
    String failure= new ComparisonCompactor(0, "abc", "adc").compact(null); 
    assertEquals("expected:<...[b]...> but was:<...[d]...>", failure);
  }

  public void testStartAndEndContext() {
    String failure= new ComparisonCompactor(1, "abc", "adc").compact(null); 
    assertEquals("expected:<a[b]c> but was:<a[d]c>", failure);
  }

  public void testStartAndEndContextWithEllipses() { 
    String failure= new ComparisonCompactor(1, "abcde", "abfde").compact(null); 
    assertEquals("expected:<...b[c]d...> but was:<...b[f]d...>", failure);
  }

  public void testComparisonErrorStartSameComplete() {
    String failure= new ComparisonCompactor(2, "ab", "abc").compact(null); 
    assertEquals("expected:<ab[]> but was:<ab[c]>", failure);
  }

  public void testComparisonErrorEndSameComplete() {
    String failure= new ComparisonCompactor(0, "bc", "abc").compact(null); 
    assertEquals("expected:<[]...> but was:<[a]...>", failure);
  }

  public void testComparisonErrorEndSameCompleteContext() {
    String failure= new ComparisonCompactor(2, "bc", "abc").compact(null); 
    assertEquals("expected:<[]bc> but was:<[a]bc>", failure);
  }

  public void testComparisonErrorOverlapingMatches() {
    String failure= new ComparisonCompactor(0, "abc", "abbc").compact(null); 
    assertEquals("expected:<...[]...> but was:<...[b]...>", failure);
  }

  public void testComparisonErrorOverlapingMatchesContext() {
    String failure= new ComparisonCompactor(2, "abc", "abbc").compact(null); 
    assertEquals("expected:<ab[]c> but was:<ab[b]c>", failure);
  }

  public void testComparisonErrorOverlapingMatches2() { 
    String failure= new ComparisonCompactor(0, "abcdde","abcde").compact(null);
  assertEquals("expected:<...[d]...> but was:<...[]...>", failure);
  }

  public void testComparisonErrorOverlapingMatches2Context() { 
    String failure=new ComparisonCompactor(2, "abcdde", "abcde").compact(null); 
    assertEquals("expected:<...cd[d]e> but was:<...cd[]e>", failure);
  }

  public void testComparisonErrorWithActualNull() {
    String failure= new ComparisonCompactor(0, "a", null).compact(null); 
    assertEquals("expected:<a> but was:<null>", failure);
  }

  public void testComparisonErrorWithActualNullContext() {
    String failure= new ComparisonCompactor(2, "a", null).compact(null);
    assertEquals("expected:<a> but was:<null>", failure); 
  }

  public void testComparisonErrorWithExpectedNull() {
    String failure= new ComparisonCompactor(0, null, "a").compact(null); 
    assertEquals("expected:<null> but was:<a>", failure);
  }

  public void testComparisonErrorWithExpectedNullContext() {
    String failure= new ComparisonCompactor(2, null, "a").compact(null); 
    assertEquals("expected:<null> but was:<a>", failure);
  }

  public void testBug609972() {
    String failure= new ComparisonCompactor(10, "S&P500", "0").compact(null); 
    assertEquals("expected:<[S&P50]0> but was:<[]0>", failure);
  }
}

```

* 위 테스트 케이스 코드 커버리지 100%?
* 아래가 코드임

### ComaparisonCompactor.java

```java
package junit.framework;
public class ComparisonCompactor {

  private static final String ELLIPSIS = "..."; 
  private static final String DELTA_END = "]"; 
  private static final String DELTA_START = "[";

  private int fContextLength; 
  private String fExpected; 
  private String fActual; 
  private int fPrefix; 
  private int fSuffix;

  public ComparisonCompactor(int contextLength, String expected, String actual) { 
    fContextLength = contextLength;
    fExpected = expected;
    fActual = actual; 
  }

  public String compact(String message) {
    if (fExpected == null || fActual == null || areStringsEqual())
      return Assert.format(message, fExpected, fActual);
      
    findCommonPrefix();
    findCommonSuffix();
    String expected = compactString(fExpected); 
    String actual = compactString(fActual);
    return Assert.format(message, expected, actual);
  }
  private String compactString(String source) { 
    String result = DELTA_START +
    source.substring(fPrefix, source.length() - fSuffix + 1) + DELTA_END;
    
    if (fPrefix > 0)
      result = computeCommonPrefix() + result;
    if (fSuffix > 0)
      result = result + computeCommonSuffix();
    return result; 
  }

  private void findCommonPrefix() {
    fPrefix = 0;
    int end = Math.min(fExpected.length(), fActual.length()); 
    for (; fPrefix < end; fPrefix++) {
      if (fExpected.charAt(fPrefix) != fActual.charAt(fPrefix)) 
        break;
    }
  }

  private void findCommonSuffix() {
    int expectedSuffix = fExpected.length() - 1; 
    int actualSuffix = fActual.length() - 1; 
    for (; actualSuffix >= fPrefix && expectedSuffix >= fPrefix; actualSuffix--, expectedSuffix--) {
      if (fExpected.charAt(expectedSuffix) != fActual.charAt(actualSuffix)) 
      break;
    }
    fSuffix = fExpected.length() - expectedSuffix; 
  }
  private String computeCommonPrefix() {
    return (fPrefix > fContextLength ? ELLIPSIS : "") + fExpected.substring(Math.max(0, fPrefix - fContextLength), fPrefix);
  }
  private String computeCommonSuffix() {
    int end = Math.min(fExpected.length() - fSuffix + 1 + fContextLength,fExpected.length());
    return fExpected.substring(fExpected.length() - fSuffix + 1, end) +
      (fExpected.length() - fSuffix + 1 < fExpected.length() - fContextLength ? ELLIPSIS : "");
  }
  private boolean areStringsEqual() { 
    return fExpected.equals(fActual);
  } 
}
  
```

* 긴 표현식 몇 개와 이상한 +1 등이 눈에 띄지만
* 전반적으로 상당히 훌륭함, 아래 처럼 짰을 수도 있음

### ComaparisonCompactor.java - defactoring
```java
package junit.framework;
public class ComparisonCompactor { 

  private int ctxt;
  private String s1;
  private String s2;
  private int pfx; 
  private int sfx;

  public ComparisonCompactor(int ctxt, String s1, String s2) { 
    this.ctxt = ctxt;
    this.s1 = s1;
    this.s2 = s2;
  }
  public String compact(String msg) {
    if (s1 == null || s2 == null || s1.equals(s2))
      return Assert.format(msg, s1, s2);
    pfx = 0;

    for (; pfx < Math.min(s1.length(), s2.length()); pfx++) {
      if (s1.charAt(pfx) != s2.charAt(pfx)) break;
    }

    int sfx1 = s1.length() - 1;
    int sfx2 = s2.length() - 1;

    for (; sfx2 >= pfx && sfx1 >= pfx; sfx2--, sfx1--) {
      if (s1.charAt(sfx1) != s2.charAt(sfx2)) break;
    }
    sfx = s1.length() - sfx1;
    String cmp1 = compactString(s1); 
    String cmp2 = compactString(s2); 
    return Assert.format(msg, cmp1, cmp2);
  }
  private String compactString(String s) { 
    String result = "[" + s.substring(pfx, s.length() - sfx + 1) + "]"; 
    if (pfx > 0)
      result = (pfx > ctxt ? "..." : "") + s1.substring(Math.max(0, pfx - ctxt), pfx) + result
    if (sfx > 0) {
      int end = Math.min(s1.length() - sfx + 1 + ctxt, s1.length()); 
      result = result + (s1.substring(s1.length() - sfx + 1, end) +
        (s1.length() - sfx + 1 < s1.length() - ctxt ? "..." : "")); 
    }
    return result; 
  }
}
```

* 멤버 변수 앞에 붙어져있는 f 접두어가 거슬린다.
* 변수 이름에 범위를 명시할 필요가 없다.

```java
private int contextLength; 
private String expected; 
private String actual; 
private int prefix; 
private int suffix;
```

* compact 함수 시작부에 캡슐화 되지 않은 조건문

```java
if(expected == null || actual == null || areStringsEqual())
  return Assert.format(message, fExpected, fActual);

if(shouldNotCompact())
  return Assert.format(message, fExpected, fActual);

private boolean shouldNotCompact() {
  return expected == null || actual == null || areStringsEqual();
}

```

* compact 함수에서 사용하는 this.expected / this.actual 도 거슬림
* 함수에 이미 expected라는 지역변수가 있는데 f를 빼버리는 바람에 생긴 결과임
* 함수에서 멤버변수와 같은 이름을 사용하는 변수를 사용하는 이유가 뭘까? 서로 다른 이름이야!

```java
String compactExpected = compactString(expected); 
String compactActual = compactString(actual);
```

* 부정문은 긍정문보다 이해하기 약간 더 어렵다.
* shouldNotCompact -> canBeCompacted

```java
public String compact(String message) { 
  if (canBeCompacted()) {
    findCommonPrefix();
    findCommonSuffix();
    String compactExpected = compactString(expected); 
    String compactActual = compactString(actual);
    return Assert.format(message, compactExpected, compactActual);
  } else {
    return Assert.format(message, expected, actual);
  } 
}
private boolean canBeCompacted() {
  return expected != null && actual != null && !areStringsEqual();
}
```

* canBeCompacted가 false면 압축을 하지 않으니, compact라느 이름ㅇ ㅣ이상하다>? 오류 점검이라는 부가 단계가 숨겨짐
* 게다가 함수는 단순 압축이 아닌 형식이 갖춰진 문자열을 반환한다.
* `formatCompactedComparision`
* if문 안에서는 예상 문자열과 실제 문자열을 진짜로 압축함. 이부분을 빼내서
* `compactExpectedAndActual` 은 압축만 수행한다.


```java

...
private String compactExpected; 
private String compactActual;

...
public String formatCompactedComparison(String message) { 
  if (canBeCompacted()) {
    compactExpectedAndActual();
    return Assert.format(message, compactExpected, compactActual); 
  } else {
    return Assert.format(message, expected, actual);
  } 
}

private void compactExpectedAndActual() { 
  findCommonPrefix();
  findCommonSuffix();
  compactExpected = compactString(expected); 
  compactActual = compactString(actual);
}

```

* 멤버변수로 승격했다.
* 새 함수에서 마지막 두줄은 변수를 반환하지만 
* 첫째 줄과 둘째 줄은 반환값이 없다. 함수 사용 방식이 일관적이지 못함


```java
private void compactExpectedAndActual() { 
  prefixIndex = findCommonPrefix(); 
  suffixIndex = findCommonSuffix(); 
  compactExpected = compactString(expected); 
  compactActual = compactString(actual);
}
private int findCommonPrefix() {
  int prefixIndex = 0;
  int end = Math.min(expected.length(), actual.length()); 
  for (; prefixIndex < end; prefixIndex++) {
    if (expected.charAt(prefixIndex) != actual.charAt(prefixIndex)) break;
  }
  return prefixIndex;
}

private int findCommonSuffix() {
  int expectedSuffix = expected.length() - 1;
  int actualSuffix = actual.length() - 1;
  for (; actualSuffix >= prefixIndex && expectedSuffix >= prefixIndex; 
    actualSuffix--, expectedSuffix--) {
    if (expected.charAt(expectedSuffix) != actual.charAt(actualSuffix))
      break; 
  }
  return expected.length() - expectedSuffix; 
}
```

* 멤버 변수 이름도 좀 더 정확하게 변경
* 결국 둘 다 색인 위치를 나타낸다.


* findCommonSuffix를 주의 깊게 보면 숨겨진 시간적인 결합
* findCommonSuffix는 findCommonPrefix가 prefixIndex를 계산한다는 사실에 의존함.
* 잘못된 순서로 호출하면 밤샘 디버깅
* 시간 결합을 외부에 노출시켜서 고친다.

```java
private void compactExpectedAndActual() { 
  prefixIndex = findCommonPrefix(); 
  suffixIndex = findCommonSuffix(prefixIndex);
  compactExpected = compactString(expected);
  compactActual = compactString(actual); 
}
private int findCommonSuffix(int prefixIndex) {
  int expectedSuffix = expected.length() - 1;
  int actualSuffix = actual.length() - 1;
  for (; actualSuffix >= prefixIndex && expectedSuffix >= prefixIndex;actualSuffix--, expectedSuffix--) {
    if (expected.charAt(expectedSuffix) != actual.charAt(actualSuffix))
      break; 
  }
  return expected.length() - expectedSuffix; 
}

```
* prefixIndex를 인수로 전달하지 만 다소 자의적이다.
* 함수 호출 순서는 확실히 정해지지만 필요한 이유는 설명하지 못한다.
* 다른 프로그래머가 다시 돌려놓을 수도 있음.


```java
private void compactExpectedAndActual() { 
  findCommonPrefixAndSuffix(); 
  compactExpected = compactString(expected); 
  compactActual = compactString(actual);
}

private void findCommonPrefixAndSuffix() { 
  findCommonPrefix();
  int expectedSuffix = expected.length() - 1; 
  int actualSuffix = actual.length() - 1; 
  for (; actualSuffix >= prefixIndex && expectedSuffix >= prefixIndex; actualSuffix--, expectedSuffix-- ){
    if (expected.charAt(expectedSuffix) != actual.charAt(actualSuffix)) break;
  }
  suffixIndex = expected.length() - expectedSuffix; 
}

private void findCommonPrefix() {
  prefixIndex = 0;
  int end = Math.min(expected.length(), actual.length()); 
  for (; prefixIndex < end; prefixIndex++)
    if (expected.charAt(prefixIndex) != actual.charAt(prefixIndex)) break;
}
```

* findCommonPrefix / findCommonSuffix를 원래대로 돌린다.
* findCommonSuffix -> findCommonPrefixAndSuffix로 변경
* 이 함수에서 findCommonPrefix를 호출

```java
private void findCommonPrefixAndSuffix() { 
  findCommonPrefix();
  int suffixLength = 1;
  for (; !suffixOverlapsPrefix(suffixLength); suffixLength++) { 
    if (charFromEnd(expected, suffixLength) != charFromEnd(actual, suffixLength)) 
    break;
  }
  suffixIndex = suffixLength; 
}
private char charFromEnd(String s, int i) { 
  return s.charAt(s.length()-i);
}
private boolean suffixOverlapsPrefix(int suffixLength) { 
  return actual.length() - suffixLength < prefixLength || expected.length() - suffixLength < prefixLength; 
}
```
* suffixIndex가 사실 접미어 길이 - length 로 변경
* computeCommonSuffix에  +1 이 곳곳에 등장하는 이유임.



```java
public class ComparisonCompactor { 

  ...

  private int suffixLength; 

  ...

  private void findCommonPrefixAndSuffix() {
    findCommonPrefix();
    suffixLength = 0;
    for (; !suffixOverlapsPrefix(suffixLength); suffixLength++) {
      if (charFromEnd(expected, suffixLength) != charFromEnd(actual, suffixLength))
        break; 
    }
  }
  private char charFromEnd(String s, int i) { 
    return s.charAt(s.length() - i - 1);
  }
  private boolean suffixOverlapsPrefix(int suffixLength) { 
    return actual.length() - suffixLength <= prefixLength || expected.length() - suffixLength <= prefixLength; 
  }

...

private String compactString(String source) {
  String result =
    DELTA_START +
      source.substring(prefixLength, source.length() - suffixLength) + DELTA_END;
  if (prefixLength > 0)
    result = computeCommonPrefix() + result;
  if (suffixLength > 0)
    result = result + computeCommonSuffix();
  return result; 
}

...

private String computeCommonSuffix() {
  int end = Math.min(expected.length() - suffixLength + contextLength, expected.length()); 
  return expected.substring(expected.length() - suffixLength, end) + (expected.length() - suffixLength < expected.length() - contextLength ? ELLIPSIS : "");
}
```

* computeCommonSuffix에서 +1을 charFromEnd에 -1을 추가, suffixOvverlapsPrefix에 <= 을 사용
* index에서 length로 변경
* `if (suffixLength>0)` 을 발견
* suffixLength가 1씩 감소했으므로 > 을 >= 으로 변경이 맞음
* \>= 는 말이 안됨! >가 맞다?
* 길이가 0인 접미어를 걸러내 첨부하지 않으므로, suffixIndex가 언제나 1 이상이라 if문이 있으나 마나였음
* 지우고 테스트 돌려보자~

~~

* 전체 함수는 위상적으로 정렬했으므로 각 함수가 사용된 직후에 정의된다.
* 이 장 초반에 했던 결정을 일부 번복하기도 했다.
* 모듈은 처음보다 조금 더 꺠끗해짐, 원래 꾸렸다는게아니라,. 이세상에 개선이 불필요한 모듈은 없다.