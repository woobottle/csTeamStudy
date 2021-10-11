# Refactoring SerialDate

  

## 돌려보자
* SerialDateTest는 커버리지가 50프로정도임
* 단위 테스트 케이스를 구현했고 92프로까지 올림?
* 경계선 오류도 고침


## 고치자
* Serial이라는 이름? SerialNumber를 사용해 클래스를 구현해서?
* 1899년 12월 30일 기준으로 경과한 날짜..?
* relativeOffset이 더 적합하다..
<br/>

* 실상은 추상 클래스임 - 구현을 암시할 필요가 전혀 없으므로 Date가 나음
* Date는 시간이므로 날짜.. Day? Day도 많음
* DayDate를 쓰기로 결정한다...
<br/>

* Comparable, Serializable을 상속하는 이유는 알겠지만 MonthConstant을 상속하는 이유는?
* 상수 모임임, 따라서 enum으로 정의하자.
* 다고치기에 오래걸림 1시간 정도 걸림
* int로 달을 받던 메서드를 Month로 변경
* isValidMonthCode 필요 없음
* monthCodeToQuarter 필요 없음
<br/>

* 불필요 주석 제거
* `EARLIEST_DATE_ORDINAL` 이 0이 아니라 2인 이유는 ,,, ms excel때문?
* SpreadsheetDate 클래스로 가야한다. SpreadsheetDate클래스만 두 변수를 사용함.
  
<br/>

* MINIMUM_YEAR_SUPPORTED와 MAXIMUM_YEAR_SUPPORTED, DayDate는 추상클래스로 구체적인 구현 정보를 포함할 필요가 없다.
* 따라서 최소 최대년도를 지정할 이유가 없다.
* 하지만 `RelativeDayOfWeekRule` 이 두 변수를 사용함, getDate로 넘어온 인수 year가 올바른지 확인할 목적
* 추상 클래스 사용자가 구현 정보를 알아야한다?
* 훼손하지 않으면서 구현 정보를 전달할 방법이 필요하다.
* DayDate를 훼손하지 않으면서 구현정보를 전달할 방법이 필요하다.
* 일반적으로 파생클래스의 인스턴스로부터 구현 정보를 가져온다.
* getDate메서드로 넘어오는 인수는 DayDate인스턴스가 아님, 하지만 이를 반환함
* 어디선가 인스턴스를 생성한다는 것
* createInstance메서드에서 ... 생성하는데,.. 일반적으로 기반 클래스(부모클래스) 는 파생클래스에(자식클래스)에 몰려야 바람직하다. 
* 따라서 ABSTRACT FACTORY 패턴으로 DayDateFactory를 만들었다.
* DayDate인스턴스를 생성하고, 최대날짜 최소날짜 등의 구현 관련 질문에도 답한다.

```java
public abstract class DayDateFactory {
  private static DayDateFactory factory = new SpreadsheetDateFactory(); 
  public static void setInstance(DayDateFactory factory) {
    DayDateFactory.factory = factory; 
  }

  protected abstract DayDate _makeDate(int ordinal);
  protected abstract DayDate _makeDate(int day, DayDate.Month month, int year); 
  protected abstract DayDate _makeDate(int day, int month, int year); 
  protected abstract DayDate _makeDate(java.util.Date date);
  protected abstract int _getMinimumYear();
  protected abstract int _getMaximumYear();

  public static DayDate makeDate(int ordinal) { 
    return factory._makeDate(ordinal);
  }

  public static DayDate makeDate(int day, DayDate.Month month, int year) { 
    return factory._makeDate(day, month, year);
  }

  public static DayDate makeDate(int day, int month, int year) { 
    return factory._makeDate(day, month, year);
  }

  public static DayDate makeDate(java.util.Date date) { 
    return factory._makeDate(date);
  }

  public static int getMinimumYear() { 
    return factory._getMinimumYear();
  }

  public static int getMaximumYear() { 
    return factory._getMaximumYear();
  } 

}
```
* createInstance -> makeDate로 변경
* 추상 메서드로 위임하는 정적 메서드는 SIGNLETON / DECORATOR, ABSTRACT FACTORY 패턴 조합
```java
public class SpreadsheetDateFactory extends DayDateFactory { 
  public DayDate _makeDate(int ordinal) {
    return new SpreadsheetDate(ordinal); 
  }
  public DayDate _makeDate(int day, DayDate.Month month, int year) { 
    return new SpreadsheetDate(day, month, year);
  }
  public DayDate _makeDate(int day, int month, int year) { 
    return new SpreadsheetDate(day, month, year);
  }
  public DayDate _makeDate(Date date) {
    final GregorianCalendar calendar = new GregorianCalendar(); 
    calendar.setTime(date);
    return new SpreadsheetDate(
      calendar.get(Calendar.DATE), DayDate.Month.make(calendar.get(Calendar.MONTH) + 1), calendar.get(Calendar.YEAR));
  }
  protected int _getMinimumYear() {
    return SpreadsheetDate.MINIMUM_YEAR_SUPPORTED;
    }
  protected int _getMaximumYear() {
  return SpreadsheetDate.MAXIMUM_YEAR_SUPPORTED;
  } 
}

```
* MINIMUM_YEAR_SUPPORTED, MAXIMUM_YEAR_SUPPORTED은 SpreadsheetDate로 옮김
<br/>

* LAST_DAY_OF_MONTH 의 쓸데없는 주석 지우고
* LAST_DAY_OF_MONTH변수는 public변수일 필요가 없다. lastDayOfMonth라는 정적 메서드에서 사용할 뿐
* AGGREGATE_DAYS_TO_END_OF_MONTH는 수상쩍음, 어디서도 안씀
* SpreadsheetDate에서만 쓰는거 또 옮기고,
* 
<br/>

* 상수 이넘으로 변환
```java
public enum WeekInMonth {
  FIRST(1), SECOND(2), THIRD(3), FOURTH(4), LAST(0); 
  public final int index;
  WeekInMonth(int index) { 
    this.index = index;
  } 
}
```

* INCLUDE_NONE, INCLUDE_FIRST, INCLUDE_SECOND, INCLUDE_BOTH 상수는 범위 끝 날짜를 범위에 포함할지 아닌지
* CLOSED, CLOSED_LEFT, CLOSED_RIGHT,  OPEN 으로 수학적 명칭으로 변경

<br/>
* getMonths가 두개나와서 하나로 합쳐서 단순화, 이름을 서술적으로 변경
* Month가 커져서 DayDate에서 분리해서 원시파일로 만들었다.
<br/>

* monthCodeToString은  한 메서드가 다른 메서드를 호출하며 플래그를 넘긴다. 플래그 인수는 바람직하지 못하다.
* 출력 형식을 선택하는 플래그는 피한다.
* 이름을 변경하고 단순화하고 Month enum으로 옮겼다?
```java
public static String monthCodeToString(final int month) {
  return monthCodeToString(month, false); 390
}

public static String monthCodeToString(final int month,
  final boolean shortened) {
  // check arguments...
  if (!isValidMonthCode(month)) {
    throw new IllegalArgumentException("SerialDate.monthCodeToString: month outside valid range.");
   }
  final String[] months; 416
  if (shortened) {
    months = DATE_FORMAT_SYMBOLS.getShortMonths();
  }else {
    months = DATE_FORMAT_SYMBOLS.getMonths();
  }
  return months[month - 1]; 425 
```

```java
public String toString() {
  return dateFormatSymbols.getMonths()[index - 1];
}
public String toShortString() {
  return dateFormatSymbols.getShortMonths()[index - 1];
}

```

* 가독성 높이기

```java
public static boolean isLeapYear(final int yyyy){
  if ((yyyy % 4) != 0){}
    return false;
  }
  else if ((yyyy % 400) == 0) {
    return true;
  }
  else if ((yyyy % 100) == 0) {
    return false;
  }
  else {
    return true;
  }
}

public static boolean isLeapYear(int year) { 
  boolean fourth = year % 4 == 0;
  boolean hundredth = year % 100 == 0;
  boolean fourHundredth = year % 400 == 0; 
  return fourth && (!hundredth || fourHundredth);
}

```

* leapYearCount는 SpreadsheetDater에 두메서드 말고 부르는 곳이 없으므로 이동
* lastDayOfMonth 는 LAST_DAY_OF_MONTH배열을 사용
* month enum에 속하므로 메서드도 옮김
```java
public static int lastDayOfMonth(Month month, int year) { 
  if (month == Month.FEBRUARY && isLeapYear(year))
    return month.lastDay() + 1; 
  else
    return month.lastDay(); 
}
```

* addDays메서드가 나오는데 이 메서드는 온갖 DayDate변수를 쓰므로 static이면 안된다.
* 그래서 인스턴스 메서드로 변경, 이 메서드는 toSerial 메서드를 호출하는데, 이를 toOrdinal로 변경
  
```java

public static SerialDate addDays(final int days, final SerialDate base) {
  final int serialDayNumber = base.toSerial() + days;
  return SerialDate.createInstance(serialDayNumber);
}

public DayDate addDays(int days) {
return DayDateFactory.makeDate(toOrdinal() + days);
}
```

* 정적 메서드에서 인스턴스 메서드로 바꾸며서, date.addDays(5)라는 표현이 date객체를 변경하는게 아니라 새 DayDate인스턴스 를 반환한다는 사실이 드러나나?
* `plusDays` 로 메서드 이름을 변경한다.

<br/>

* 임시 변수 설명을 사용해 더 일기 쉽게 고치고 
* 정적 메서드를 인스턴스메서드로 변경,
* 중복된 인스턴스메서드 제거


getPreviousDayOfWeek
```java
public static SerialDate getPreviousDayOfWeek(final int targetWeekday,
  final SerialDate base) {
  // check arguments...
  if (!SerialDate.isValidWeekdayCode(targetWeekday)) {
    throw new IllegalArgumentException("Invalid day-of-the-week code.");
  }
  // find the date...
  final int adjust;
  final int baseDOW = base.getDayOfWeek();
  if (baseDOW > targetWeekday) {
    adjust = Math.min(0, targetWeekday - baseDOW);
  }else {
    adjust = -7 + Math.max(0, targetWeekday - baseDOW);
  }
  return SerialDate.addDays(adjust, base); 659
}

public DayDate getPreviousDayOfWeek(Day targetDayOfWeek) {
  int offsetToTarget = targetDayOfWeek.index - getDayOfWeek().index; 
  if (offsetToTarget >= 0)
    offsetToTarget -= 7;
  return plusDays(offsetToTarget);
}

```

* 테케에서만 쓰는 메서드도 지우고~ 
* getYYYY, getMonth, getDayOfMonth는 추상 메서드이며
* getDayOfWeek도 SpreadsheetDate구현에 의존하지 않으므로 DayDate로 끌어올린다?
* 논리적인 의존성이 있다.
* 물리적인 의존성이 없으므로 이도 구현해준다?

```java
public int getDayOfWeek() {
  return (this.serial + 6) % 7 + 1;
}

public Day getDayOfWeek() {
  Day startingDay = getDayOfWeekForOrdinalZero();
  int startingOffset = startingDay.index - Day.SUNDAY.index; 
  return Day.make((getOrdinalDay() + startingOffset) % 7 + 1);
}
```
* getDayOfWeekForOrdinalZero라는 추상메서드를 구현하고, SpreadsheetDate에서 Day.SATURDAY를 반환하도록 구현
* getDayOfWeek을 DayDate로 옮기고, getOrdinalDay와 getDayOfWeekForOrdinalZero를 호출하게 변경
  


### 정리
* 처음에 나오는 주석은 너무 오래됨 간단하게 고치고 개선
* enum을 모두 독자적인 소스 파일로 옮겼다.
* 정적변수와 정적메서드를 DateUtil이라는 새 클래스에 옮김. 
* 일부 추상 메서드를 DayDate클래스로 끌어 올렸다. 
* Month.make 를 Month.fromInt로 변경, 다른쪽 enum도 똑같이.
* 모든 enum에 toInt() 접근자를 생성, index 필드를 private으로
* plusYears / plusMonths에 흥미로운 중복을 correctLastOfMonth라는 메서드로 중복을 없앴다.
* 숫자 1을 뿌심, 
* 코드 커버리지는 84.9%로 감소함, 테스트하는 코드가 줄어서가 아닌 클래스 크기가 작아져서 테스트하지 않는 코드의 비중ㅇ ㅣ커짐
* 