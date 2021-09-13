# 4. 주석

* 주석은 악이고, 기껏해야 필요악이다. 주석 없이는 표현할 방법을 찾지 못해 할 수 없이 주석을 사용한다.
* 코드는 변화하고 진화하지만 주석이 따라가지 않으니 분리되어 멀어지고, 이해를 방해한다.
* 엄껵하게 관리하기보다, 애초에 필요 없는 방향으로 에너지를 쏟겠다.

### Comments Do Not Make Up for Bad Code

* 주석을 추가하는 이유는 코드 품질이 나쁘기 때문
* 표현혁이 풍부하고 깔끔하며 주석이 거의 없는 코드가 복잡하고 어수선하며 주석이 많이 달린 코드보다 훨씬 좋다.

### Explain Yourself in Code

* 코드만으로 의도를 설명하기 어려운 경우가 존재한다.

```java
// Check to see if the employee is eligible for full benefits 
if ((employee.flags & HOURLY_FLAG) && (employee.age > 65))
```

vs

```java
if (employee.isEligibleForFullBenefits())
```

* 하지만 몇초만 더 생각하면 가능함 ㅎ



## Good Comments

* 글자값 하는 주석 소개한다.
* 하지만 제일 좋은건 달지 않을 방법을 찾아낸 주석임

### Legal Comments

* 회사가 정립한 구현 표준에 맞춰 법적인 이유로 특정 주석을 넣으라고 명시한다.
* ex) 파일 첫 머리에 저작권 정보와 소유권 정보

```java
// Copyright (C) 2003,2004,2005 by Object Mentor, Inc. All rights reserved.
// Released under the terms of the GNU General Public License version 2 or later.
```

### Informative Comments

* 기본적인 정보를 제공하면 편리하다.

* ```java
  // Returns an instance of the Responder being tested.
  protected abstract Responder responderInstance();
  ```

  * 가능하면 함수 이름에 정보를 담는게 더 좋다.
  * `responderBeingTested`

  

* ```java
  // format matched kk:mm:ss EEE, MMM dd, yyyy 
  Pattern timeMatcher = Pattern.compile("\\d*:\\d*:\\d* \\w*, \\w* \\d*, \\d*");
  ```

  * 정규표현식이 시각과 날짜를 뜻한다고 설명한다.
  * 시각과 날짜를 변환하는 클래스로 만들어 코드를 옮겨주면 더 좋고 더 깔끔하다.

### Explanation of Intent

* 결정에 깔린 의도까지 설명한다.

```java
public int compareTo(Object o) {
	if(o instanceof WikiPagePath) {
		WikiPagePath p = (WikiPagePath) o;
		String compressedName = StringUtil.join(names, ""); 
    String compressedArgumentName = StringUtil.join(p.names, ""); 
    return compressedName.compareTo(compressedArgumentName);
	}
  return 1; // we are greater because we are the right type. 
}
```

* 작성자는 두 객체를 비교할 때 자기 객체에 더 높은 우선순위를 주기로 결정함
* 

```java
public void testConcurrentAddWidgets() throws Exception { 
  WidgetBuilder widgetBuilder = new WidgetBuilder(new Class[]{BoldWidget.class});
	String text = "'''bold text'''"; 
  ParentWidget parent = new BoldWidget(new MockWidgetRoot(), "'''bold text'''"); 
  AtomicBoolean failFlag = new AtomicBoolean(); 
  failFlag.set(false);
	//This is our best attempt to get a race condition 
  //by creating large number of threads.
	for (int i = 0; i < 25000; i++) {
		WidgetBuilderThread widgetBuilderThread = new WidgetBuilderThread(widgetBuilder, text, parent, failFlag);
		Thread thread = new Thread(widgetBuilderThread);
		thread.start(); 
  }
	assertEquals(false, failFlag.get()); 
}
```



### Clarification

* 인수나 반환값이 그 의미를 읽기 좋게 표현하면 쉬워진다, 자체를 명확하게 만들면 더 좋지만
* 표준 라이브러리나 변경하지 못하는 코드에 속하면 의미를 명료하게 밝히는 주석이 유용하다

```java
public void testCompareTo() throws Exception {
	WikiPagePath a = PathParser.parse("PageA"); 
  WikiPagePath ab = PathParser.parse("PageA.PageB"); 
  WikiPagePath b = PathParser.parse("PageB"); 
  WikiPagePath aa = PathParser.parse("PageA.PageA"); 
  WikiPagePath bb = PathParser.parse("PageB.PageB"); 
  WikiPagePath ba = PathParser.parse("PageB.PageA");
  assertTrue(a.compareTo(a) == 0);    // a == a 
  assertTrue(a.compareTo(b) != 0);    // a != b 
  assertTrue(ab.compareTo(ab) == 0);  // ab == ab 
  assertTrue(a.compareTo(b) == -1);   // a < b 
  assertTrue(aa.compareTo(ab) == -1); // aa < ab 
  assertTrue(ba.compareTo(bb) == -1); // ba < bb 
  assertTrue(b.compareTo(a) == 1);    // b > a 
  assertTrue(ab.compareTo(aa) == 1);  // ab > aa 
  assertTrue(bb.compareTo(ba) == 1);  // bb > ba
}
```

* 주석이 올바른지 검증하기 쉽지 않다. 따라서 의미를 명료하게 밝히는게 필요하며, 주석이 위험한 이유
* 더 나은 방법이 없는지 고민하고 정확하게 달도록 한다.



### Warning of Consequences

* 경고 목적의 주석

* ```java
  // Don't run unless you
  // have some time to kill.
  public void _testWithReallyBigFile() {
  	writeLinesToFile(10000000);
  	response.setBody(testFile);
  	response.readyToSend(this);
  	String responseString = output.toString(); 
    assertSubString("Content-Length: 1000000000", 	responseString); 
    assertTrue(bytesSent > 1000000000);
  }
  
  ```

* 요즘은 `@Ignore` 속성을 이용해 테케를 꺼버림, 문자열로 설명을 넣어줌

```java

public static SimpleDateFormat makeStandardHttpDateFormat() {
	//SimpleDateFormat is not thread safe,
	//so we need to create each instance independently.
	SimpleDateFormat df = new SimpleDateFormat("EEE, dd MMM yyyy HH:mm:ss z");
  df.setTimeZone(TimeZone.getTimeZone("GMT"));
  return df;
}

```

## Todo Comments

```java
//TODO-MdM these are not needed
// We expect this to go away when we do the checkout model 
protected VersionInfo makeVersion() throws Exception
{
	return null; 
}
```

* 나쁜 코드를 남겨두는 핑계가 되선 안됨
* 주기적으로 점검해 뿌시셈

### Amplification

강조 

* 대수롭지 않다고 여겨질 뭔가의 중요성을 강조하기 위해서 사용함

  ```java
  String listItemContent = match.group(3).trim();
  // the trim is real important. It removes the starting 
  // spaces that could cause the item to be recognized
  // as another list.
  new ListItemWidget(this, listItemContent, this.level + 1);
  return buildList(text.substring(match.end()));
  ```

### javadocs in public apis

공개 api를 구현한다면 반드시 훌륭한 javadocs를 작성한다.



## Bad Comments

주절거리는 주석

* 이유없이 의무감으로 혹은 하라고하니까 주석 달면 시간낭비다.

* ```java
  public void loadProperties() {
  	try {
  		String propertiesPath = propertiesLocation + "/" + PROPERTIES_FILE; 
  	  FileInputStream 	propertiesStream = new FileInputStream(propertiesPath); 		
      loadedProperties.load(propertiesStream);
  	}
  	catch(IOException e) {
  	// No properties files means all defaults are loaded
  	} 
  }
  ```

  * 파일이 없다는거임, 그럼 모두 기본값으로 읽어들였단다?
  * 기본값을?? 호출하기 전에 ?  후에 ? 언제하나
  * 알려면 다른 코드를 뒤져야함

  

* ```java
  // 4-1
  // Utility method that returns when this.closed is true. Throws an exception 
  // if the timeout is reached.
  public synchronized void waitForClose(final long timeoutMillis)
  	throws Exception {
  		if(!closed) {
  			wait(timeoutMillis); 
        if(!closed)
  				throw new Exception("MockResponseSender could not be closed"); 
      }
  }
  ```

  * 코드보다 더 많은 정보를 제공하지 못한다.
  * 코드를 정당화하는 주석도 아니고, 의도나 근거를 설명하는 주석도 아니다.
  * 코드보다 읽기 쉽지않다.

### Misleading Comments

* 4-1 에서 closed가 true로 변하는 순간에 반환되지 않음, true면 반환되는거임
* 타임아웃을 기다렸다가, closed가 true가 아니면 예외를 던진다.
* 주석에 담긴 살짝 잘못된 정보로 인해 closed가 true로 변하는 순간에 함수가 반환된다고 생각하는 프로그래머가 있을 수 있음
* 

### Mandated Comments - 의무적으로 다는 주석

* 모든 함수에 혹은 변수에 주석을 달아야 한다는 규칙은 어리석다.

* 오히려 복잡하고 거짓말하고 혼동과 무질서를 초래함

* ```java
  /** *
  * @param title The title of the CD
  * @param author The author of the CD
  * @param tracks The number of tracks on the CD
  * @param durationInMinutes The duration of the CD in minutes */
  public void addCD(String title, String author,int tracks, int durationInMinutes) {
  	CD cd = new CD(); 
    cd.title = title; 
    cd.author = author; 
    cd.tracks = tracks; 
    cd.duration = duration; 
    cdList.add(cd);
  }
  ```



### Journal Comments - 이력을 기록하는 주석

* 예전에는 변경 이력을 기록하고 관리하는 관례가 바람직 했지만 요즘엔 소스코드 관리 시스템이 있으니 혼란만 가중시킨다.

### Noise Comments - 있으나 마나

* 당연한 사실을 언급하고 새로운 정보를 주지못하는 주석

* ```java
  /**
  * Default constructor. 
  */
  protected AnnualDateRule() { }
  
  /** The day of the month. */
  private int dayOfMonth;
  
  /**
  * Returns the day of the month. 
  *
  * @return the day of the month. 
  */
  public int getDayOfMonth() { 
    return dayOfMonth;
  }
  ```

  * 지나친 참견이라, 개발자가 주석을 무시하는 습관에 빠진다.



* ```java
  //4-4 StartSending
  private void startSending() {
  	try {
  		doSending(); 
    }
  	catch(SocketException e) {
  		// normal. someone stopped the request.
  	}
  	catch(Exception e) {
  		try {
  			response.add(ErrorResponder.makeExceptionString(e));
  			response.closeAll(); 
      }
  		catch(Exception e1) {
  			//Give me a break!
  		} 
    }
  }
  ```

  * 첫 catch는 무시해도 괜찮은 이유를 설명하는 주석이다.
  * 두번째는 쓸모가 없다.

  ```java
  //4-5 startSending ( refactored )
  private void startSending(){
  	try {
      doSending(); 
    }
    catch(SocketException e) {
      // normal. someone stopped the request. 
    }
    catch(Exception e) {
  	  addExceptionAndCloseResponse(e); 
    }
  }
  private void addExceptionAndCloseResponse(Exception e) {
    try {
    	response.add(ErrorResponder.makeExceptionString(e));
  	  response.closeAll(); 
    }
    catch(Exception e1) {
    }
  }
  
  ```

  * 독자적인 함수로 만드는 데 노력을 쏟았어야함

### Scary Noise

* ```java
  
  /** The name. */ 
  private String name;
  /** The version. */ 
  private String version;
  /** The licenceName. */ 
  private String licenceName;
  /** The version. */ 
  private String info;
  ```



## Don't Use a Comment When You Can User a Function or a Variable

함수나 변수로 표현할 수 있다면 주석을 달지 마라

```java
// does the module from the global list <mod> depend on the
// subsystem we are part of?
if (smodule.getDependSubsystems().contains(subSysMod.getSubSystem()))
```



```java
ArrayList moduleDependees = smodule.getDependSubsystems(); 
String ourSubSystem = subSysMod.getSubSystem();
if (moduleDependees.contains(ourSubSystem))
```



### Position Markers

```java
// Actions //////////////////////////////////
```

* 반드시 필요할때만, 아주 드물게 사용하는게 좋다.



### Closing Brace Comments

* 닫는 괄호에 특수한 주석을 달아놓는데, 중첩이 심하고 장황하면 모르겠지만
* 우리가 선호하는 코드는 작고 캡슐화 된거라서 잡음일 뿐 , 그거 다드니 함수를 줄여라



### Attributions and Bylines

* 소스 코드 관리 시스템이 알아서 하는데 굳이 저자의 이름을 추가할 필요가 있나.



## Commented-Out Code

* 주석으로 처리한 코드 
* 다른 사람들이 지우기를 주저한다. 이유가 있어 남겼으리라,
* 소스 코드 관리 시스템이 우리를 대신해 코드를 기억하므로 그럴 필요 없다.

### HTML comments

* html 주석은 편집기/IDE 에서 조차 읽기 어렵다.

### Nonlocal Information

* 지역적인 것만 기술해라, 시스템 전반의 정보를 기술하지 마라

* ```java
  /**
  * Port on which fitnesse would run. Defaults to <b>8082</b>. 
  *
  * @param fitnessePort
  */
  public void setFitnessePort(int fitnessePort) {
  	this.fitnessePort = fitnessePort; 
  }
  ```

  * 어차피 함수는 포트 기본값을 전혀 통제하지 못한다.
  * 즉 아래 함수가 아닌 다른 함수를 설명하는 것임
  * 포트 기본값이 변경되어도 아래 주석이 변하리라는 보장은 못함

### Too Much Information

* RFC 번호를 제외하면 불필요하고 불가사의함

  ```java
  
  /*
  RFC 2045 - Multipurpose Internet Mail Extensions (MIME)
  Part One: Format of Internet Message Bodies
  section 6.8. Base64 Content-Transfer-Encoding
  The encoding process represents 24-bit groups of input bits as output strings of 4 encoded characters. Proceeding from left to right, a 24-bit input group is formed by concatenating 3 8-bit input groups. These 24 bits are then treated as 4 concatenated 6-bit groups, each of which is translated into a single digit in the base64 alphabet. When encoding a bit stream via the base64 encoding, the bit stream must be presumed to be ordered with the most-significant-bit first. That is, the first bit in the stream will be the high-order bit in the first 8-bit byte, and the eighth bit will be the low-order bit in the first 8-bit byte, and so on.
  */
  ```

### Inobvious Connection

* 코드와 주석 사이의 관계가 명백해야한다.

* ```java
  /*
  * start with an array that is big enough to hold all the pixels 
  * (plus filter bytes), and an extra 200 bytes for header info 
  */
  this.pngBytes = new byte[((this.width + 1) * this.height * 3) + 200];
  
  ```

  * 필터 바이트가 뭔가? +1인가? *3인가? 아니면 둘다? 
  * 

### Function Headers

* 짧은 함수는 긴 설명이 필요없다.
* 짧고 한가지만 수행하며 이름을 잘 붙였으면 주석으로 헤더를 추가한 함수보다 훨씬 좋음



```java
// 4-7 GeneratePrimes.java	
/**
* This class Generates prime numbers up to a user specified
* maximum. The algorithm used is the Sieve of Eratosthenes.
* <p>
* Eratosthenes of Cyrene, b. c. 276 BC, Cyrene, Libya --
* d. c. 194, Alexandria. The first man to calculate the
* circumference of the Earth. Also known for working on
* calendars with leap years and ran the library at Alexandria.
* <p>
* The algorithm is quite simple. Given an array of integers
* starting at 2. Cross out all multiples of 2. Find the next
* uncrossed integer, and cross out all of its multiples.
* Repeat untilyou have passed the square root of the maximum
* value. 
*
* @author Alphonse
* @version 13 Feb 2002 atp 
*/
import java.util.*;
public class GeneratePrimes {
  /**
  * @param maxValue is the generation limit. 
  */
  public static int[] generatePrimes(int maxValue) {
    if (maxValue >= 2) // the only valid case 
    {
      // declarations
      int s = maxValue + 1; // size of array 
      boolean[] f = new boolean[s];
      int i;
      // initialize array to true. 
      for (i = 0; i < s; i++)
        f[i] = true;
      // get rid of known non-primes 
      f[0] = f[1] = false;
      
      // sieve
      int j;
      for (i = 2; i < Math.sqrt(s) + 1; i++) {
        if (f[i]) // if i is uncrossed, cross its multiples. 
        {
          for (j = 2 * i; j < s; j += i)
	          f[j] = false; // multiple is not prime
        } 
      }
      // how many primes are there? 
      int count = 0;
      for (i = 0; i < s; i++) {
        if (f[i])
          count++; // bump count.
      }
      int[] primes = new int[count];
      // move the primes into the result 
      for (i = 0; j = 0; i < s; i++)
      {
        if (f[i]) //if prime
          primes[j++] = i;
      }
    }
    return primes; // return the primes
  }
  else // maxValue < 2
    return new int[0];// return null array if bad input.
  }
}
  
```





```java
/**
* This class Generates prime numbers up to a user specified 
* maximum. The algorithm used is the Sieve of Eratosthenes. 
* Given an array of integers starting at 2:
* Find the first uncrossed integer, and cross out all its
* multiples. Repeat until there are no more multiples 
* in the array.
*/
public class PrimeGenerator {
  private static boolean[] crossedOut; 
  private static int[] result;

  public static int[] generatePrimes(int maxValue) {
    if (maxValue < 2) 
      return new int[0];
    else {
      uncrossIntegersUpTo(maxValue); 
      crossOutMultiples(); 
      putUncrossedIntegersIntoResult(); 
      return result;
    } 
  }
  private static void uncrossIntegersUpTo(int maxValue) {
    crossedOut = new boolean[maxValue + 1]; 
    for (int i = 2; i < crossedOut.length; i++)
      crossedOut[i] = false; 
  }
  private static void crossOutMultiples() {
    int limit = determineIterationLimit(); 
    for (int i = 2; i <= limit; i++)
      if (notCrossed(i)) crossOutMultiplesOf(i);
  }
  private static int determineIterationLimit() {
  // Every multiple in the array has a prime factor that 
  // is less than or equal to the root of the array size, 
  // so we don't have to cross out multiples of numbers 
  // larger than that root.
    // 배열에 있는 모든 배수는 배열 크기의 제곱근보다 작은 소수의 인수이다.
    // 따라서 이 제곱근보다 더 큰 숫자의 배수는 제거할 필요가 없다,
    double iterationLimit = Math.sqrt(crossedOut.length);
    return (int) iterationLimit; 
  }
  private static void crossOutMultiplesOf(int i) {
    for (int multiple = 2*i; multiple < crossedOut.length; multiple += i)
      crossedOut[multiple] = true; 
  }
  private static boolean notCrossed(int i) {
    return crossedOut[i] == false; 
  }
  private static void putUncrossedIntegersIntoResult() {
    result = new int[numberOfUncrossedIntegers()]; 
    for (int j = 0, i = 2; i < crossedOut.length; i++)
      if (notCrossed(i)) result[j++] = i;
  }
  private static int numberOfUncrossedIntegers() {
    int count = 0;
    for (int i = 2; i < crossedOut.length; i++)
      if (notCrossed(i)) count++;
    return count; 
  }
}

```

* 첫 주석은 중복이라고 생각할 수 도 있지만, 알고리즘 이해를 위해 남겾둠
* 두 번째 주석은 거의 확실히 필요하다, 루프 한계값으로 제곱근을 사용한 이유를 설명한다.
* 변수 이름을 바꾸거나 코드 구조를 조정해 이유를 명확하게 설명할 방법을 찾지 못함
* 제곱근 사용은 자신만의 생각일지도 모른다, 제곱근까지만 루프를 돌면 정말 시간을 절약할까?오히려 더드는거 아닌가?









