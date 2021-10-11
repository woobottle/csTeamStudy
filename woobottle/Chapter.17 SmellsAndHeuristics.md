# 17. SmellsAndHeuristics

### 주석
**C1: 부적절한 정보**
일반적으로 작성자, 최종 수정일, SPR번호 등과 같은 메타정보만 주석으로 넣는다.

**C2: 쓸모 없는 주석**
쓸모 없어진 주석은 아예 삭제

**C3: 중복된 주석**
`i++ // i 증가` => 이런거 필요 x

**C4: 성의 없는 주석**
주절 대지 않고 당연한 소리 하지 않고 주석은 깔끔하게 작성

**C5: 주석 처리된 코드**
주석으로 처리된 코드들은 쓰지 않는 거면 바로 지워버리자.


### 환경
**E1: 여러 단계로 빌드해야 한다**
빌드는 간단히 한 단계로 끝나야 한다.

**E2: 여러 단계로 테스트해야 한다**
모든 단위 테스트는 한 명령으로 돌려야 한다

### 함수
**F1: 너무 많은 인수**
인수는 적을수록 좋다. 네개 이상이라면 의심하라

**F2: 출력 인수**
함수에서 뭔가의 상태를 변경해야 한다면 함수가 속한 객체의 상태를 변경한다.

**F3: 플래그 인수**
플래그 인수는 피해야 마땅하다

**F4: 죽은 함수**
아무도 호출하지 않는 함수는 삭제한다

### 일반
**G1: 한 소스 파일에 여러 언어를 사용한다.**
한 소스 파일 내에서 하나의 언어로 작성할 수 있도록 노력해야 한다.

**G2: 당연한 동작을 구현하지 않는다.**
함수나 클래스는 다른 프로그래머가 당연하게 여길만한 동작과 기능을 제공해야 한다.
`Day day = DayDate.StringToDay(String dayName)` => 이 함수는 'Monday'를 Day.MONDAY로 바꿀걸로 예상이 된다. 
이와 같이 예상되는 함수를 구현해야 한다.

**G3: 경계를 올바로 처리하지 않느다**
모든 경계 조건을 찾고 모든 경계 조건을 테스트 하는 테스트 케이스를 작성하라

**G4: 안전 절차 무시**
실패하는 테스트 케이스를 일단 제껴두고 나중으로 미루는 태도는 신용카드가 공짜 돈이라는 생각만큼 위험하다

**G5: 중복**
어디서든 중복을 발견하면 없애자

**G6: 추상화 수준이 올바르지 못하다**
추상화로 개념을 분리할때는 철저해야 한다. 모든 저차원 개념은 파생 클래스에, 모든 고차원 개념은 기초 클래스에 넣는다.

**G7: 기초 클래스가 파생 클래스에 의존한다.**
기초 클래스는 파생 클래스보다 상위 개념이다. 기초 클래스는 파생 클래스를 몰라야 한다.

**G8: 과도한 정보**
잘 정의된 인터페이스는 많은 함수를 제공하지 않는다. 그래서 결합도가 낮다.
클래스가 제공하는 메서드는 작을수록 좋다.

**G9: 죽은 코드**
사용되지 않는 코드를 발견하면 바로 삭제 해라

**G10: 수직 분리**
변수와 함수는 사용되는 위치에 가깝게 정의한다. 지역 변수는 처음으로 사용하기 직전에 선언하며 수직으로 가까운 곳에 위치해야 한다.

**G11: 일관성 부족**
유사한 개념끼리는 같은 방식으로 구현이 되어야 한다. 유사한 이름 또한 써야한다

**G12: 잡동사니**
소스파일은 깔끔하게 유지하자

**G13: 인위적 결합**
서로 무관한 개념을 결합하려 하지 말자. 불 필요한 클래스들이나 변수만 더 생길 뿐이다.

**G14: 기능욕심**
클래스 메서드는 자기 클래스의 변수와 함수에 관심을 가져야지 다른 클래스의 것을 욕심내면 안된다

```java
public class HourlyPayCalculator {
  public Money calculateWeeklyPay(HourlyEmpoyee e) {
    int tenthRate = e.getTenthRate().getPeenies();
    int tenthsWorked = e.getTenthsWorked();
    int straightTime = Math.min(400, tenthsWorked);
    int overTime = Math.max(0, tenthsWorked - straightTime);
    int straightPay = straightTime * tenthRate;
    int overtimePay = (int)Math.round(overTime*tenthRate*1.5);
    return new Money(straightPay + overtimePay);
  }
}
```
=> calculateWeeklyPay 메서드는 자기자신이 HourlyEmployy의 메서드이길 바란다.


**G15: 선택자 인수**
함수의 인자로 boolean 값을 보내는 것을 최대한 지양하자

좋지 못한 예
```java
public int calculateWeeklyPay(boolean overtime) {
  int tenthRate = getTenthRate();
  int tenthsWorked = getTenthsWorked();
  int straightTime = Math.min(400, tenthsWorked);
  int overTime = Math.max(0, tenthsWorked - straightTime);
  int straightPay = straightTime * tenthRate;
  double overtimeRate = overTime ? 1.5 : 1.0 * tenthRate;
  int overtimePay = (int)Math.round(overTime*overtimeRate);
  return straightPay + overtimePay;
}
```

```java
public int straightPay() {
  return getTEnthsWorked() * getTenthRate();
}

public int overTimePay() {
  int overTimeTenths = Math.max(0, getTenthsWorked() - 400);
  int overTimePay = overTimeBonus(overTimeTenths);
  return straightPay() + overTimePay;
}

public int overTimeBonus(int overTimeTenths) {
  double bonus = 0.5 * getTenthRate() * overTimeTenths;
  return (int)Math.round(bonus);
}
```

**G16: 모호한 의도**
코드를 짤 때는 의도를  최대한 분명히 밝혀야 한다.
아래의 함수는 최악이다
```java
public int m_otCalc{
  return iThsWkd * iThsRte + (int)Math.round(0.5 * iThsRte * Math.max(0, iThsWkd - 400));
  }
}
```

**G17: 잘못 지운 책임**
코드는 독자가 자연스럽게 기대할 위치에 배치한다.
개발자에게 편한 위치에 알맞은 기능을 넣어야 한다.(마치 책을 읽듯이)

**G18: 부적절한 static 함수**
static으로 정의되면 안되는 함수를 static으로 정의하면 안된다.
`HourlyPayCalculator.calculatePay(employee, overtimeRate)` 
위의 함수는 괜찮아 보이지만 calculatePay가 overtime일때와 아닐때로 함수를 분리하고 싶어질지도 모른다. 
조금이라도 의심스럽다면 인스턴스 함수로 정의한다.

**G19: 서술적 변수**
코드의 가독성을 높이기 위해 중간에 서술적 변수를 추가한다.
```java
Matcher match = headerPattern.matcher(line);
if(match.find()) {
  String key = match.group(1);
  String value = match.group(2);
  headers.put(key.toLowerCase(), value);
}
```

**G20: 이름과 기능이 일치하는 함수**
함수의 이름과 기능은 일치해야 한다.
`Date newDate = date.add(5)` 이 예시는 매우 좋지 못하다.
5일을 더하는 것인지, 5주를 더하는 것인지 알 수가 없다.

**G21: 알고리즘을 이해하라**
구현이 끝났다고 선언하기 전에 함수가 돌아가는 방식을 확실히 이해하는지 확인하라(개인적으로 현재 필요하다고 생각하는 부분)

**G22: 논리적 의존성은 물리적으로 드러내라**
```java
public class HourlyReporter {
  private HourlyReportFormatter formatter;
  private List<LineItem> page;
  private final int PAGE_SIZE = 55;

  public HourlyReporter(HourlyReporterFormatter formatter) {
    this.formatter = formatter;
    page = new ArrayList<LineItem>();
  }

  public void generateReport(List<HourlyEmployee> employees) {
    for (HourlyEmployee e : employees) {
      addLineItemToPage(e);
      if (page.size() == PAGE_SIZE)
        printAndClearItemList();
    }
    if (page.size() > 0) 
      printAndClearItemList();
  }

  private void printAndClearItemList() {
    formatter.format(page);
    page.clear();
  }

  private void addLineITemToPage(HourlyEmployee e){
    LineItem item = new LineItem();
    item.name = e.getName();
    item.hours = e.getTenthsWorked() / 10;
    item.tenths = egetTenthsWorked() % 10;
    page.add(item);
  }

  public class LineItem {
    public String name;
    public int hours;
    public int tenths;
  }
}
```
위 코드는 PAGE_SIZE 상수에 논리적인 의존성이 존재한다.
HourlyReporterFromatter 구현중 하나가 페이지 크기 55를 제대로 처리하지 못한다면 오류가 생긴다.
이 상수를 쓰는 대신 getMaxPAgeSize() 함수를 사용해서 물리적인 의존성으로 변화시키자

**G23: If/Else 혹은 Switch/Case 문보다 다형성을 사용하라**
선택 유형 하나에는 switch 문을 한 번만 사용한다. 
같은 선택을 수행하는 다른 코드에서는 다형성 객체를 생성해 switch문을 대신한다.

**G24: 표준 표기법을 따르라**
팀은 표준 표기법을 따라야 한다.
표준을 설명하는 문서는 코드 자체로 충분해야 하며 별도 문서를 만들 필요는 없어야 한다.

**G25: 매직 숫자는 명명된 상수로 교체하라**
일반적으로 코드에서 숫자를 사용하지 말라는 규칙이다.

**G26: 정확하라**
코드에서 뭔가를 결정할 때는 정확히 결정한다. 결정을 내리는 이유와 예외를 처리할 방법을 분명히 알아야 한다. 
코드에서 모호성과 부정확은 의견차나 게으름의 결과다. 

**G27: 관례보다 구조를 사용하라**
실제 결정을 강제할때는 규칙보다 관례를 사용한다. 명명 관례도 좋지만 구조 자체로 강제하면 더 좋다.

**G28: 조건을 캡슐화 하라**
```java
// 좋은 예
if (shouldBeDeleted(timer))

// 나쁜 예
if(timer.hasExpired() && !timer.isRecurrent(())
```

**G29: 부정 조건은 피하라**
조건문 내부는 가능하면 긍정 조건으로 표현한다.
부정 조건은 파악하기가 힘들다

**G30: 함수는 한 가지만 해야 한다**
```java
public void pay() {
  for (Employee e : employees) {
    if (e.isPayday()) {
      Money pay = e.calculatePay();
      e.deliverPay(pay);
    }
  }
}
```
위 코드는 세가지 임무를 수행함. 
아래와 같이 함수 셋으로 나눈다

```java
public void pay() {
  for (Employee e : employees) 
    payIfNecessary(e);
}

private void payIfNecessary(Employee e) {
  if (e.isPayDay())
    calculateAndDeliverPay(e)
}

private void calculateAndDeliverPay(Employee e) {
  Money pay = e.calculatePay();
  e.deliverPay(pay);
}
```
핵심은 한 개의 함수는 하나의 기능만 수행해야 한다.

**G31: 숨겨진 시간적인 결합**
시간적인 결합을 숨겨서는 안 된다.

```java
public class MoogDiver {
  Gradient gradient; 
  List<Spline> splines;

  public void dive(String reason) {
    saturateGradient();
    reticulateSplines();
    diveForMoog(reason);
  }
}
```
dive내부의 실행되는 함수들의 순서가 중요한 코드이다.
아래의 코드가 더 좋다
```java
public class MoogDiver {
  Gradient gradient;
  List<Spline> splines;

  public void dive(String reason) {
    Gradient gradient = saturateGradient();
    List<Spline> splines = reticulateSplines(gradient);
    diveForMoog(splines, reason)
  }
}
```
시간적인 결합이 필요한 부분을 오히려 노출시킨다.

**G32: 일관성을 유지하라**
코드 구조를 잡을 때는 이유를 고민하라. 그리고 그 이유를 코드 구조로 명백히 표현하라

**G33: 경계 조건을 캡슐화 하라**
코드 여기저기에 +1 이나 -1을 뿌려놓지 않는다.
```java
int nextLevel = level + 1
if(nextLevel < tags.length) {
  parts = new Parse(body, tags, nextLevel, offset + endTag);
  body = null;
}
```

**G34: 함수는 추상화 수준을 한 단계만 내려가야 한다.**
함수 내 모든 문장은 추상화 수준이 동일해야 한다. 

```java
public String render() throws Exception {
  StringBuffer html = new StringBuffer("<hr");
  if (size > 0)
    html.append(" size=\"").append(size + 1).append("\"");
  html.append(">")

  return html.toString();
}
```

```java
public String render() throws Exception {
  HtmlTag hr = new HtmlTag("hr");
  if (extraDashes > 0) 
    hr.addAttribute("size", hrSize(extraDashes));
  return hr.html();
}

private String hrSize(int height) {
  int hrSize = height + 1;
  return String.format("%d", hrSize);
}
```

**G35: 설정 정보는 최상위 단계에 둬라**
기본값 상수나 설정 관련 상수를 저차원 함수에 숨겨서는 안 된다.

```java
public static void main(String[] args) throws Exception {
  Arguments arguments = parseCommandLine(args);
}

public class Arguments {
  public static final String DEFAULT_PATH = ".";
  public static final String DEFAULT_ROOT = 'FitNessRoot';
  public static final int DEFAULT_PORT = 80;
  public static final int DEFAULT_VERSION_DAYS = 14;
}
```

안드로이드 에서 작성하는 것처럼

**G36: 추이적 탐색을 피하라**
한 모듈은 주변 모듈을 모를수록 좋다.
'A가 B를 사용하고 B가 C를 사용하더라도 A가 C를 알 필요는 없다' => 디미터의 법칙
제일 핵심은 자신이 직접 사용하는 모듈만 알아야 한다.
