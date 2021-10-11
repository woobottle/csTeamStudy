# Smells and heuristics

## Comments
1. **Inappropriate Information - 부적절한 정보**
2. **Obsolete Comment - 쓸모 없는 주석**
3. **Redundant Comment - 중복된 주석**
4. **Poorly Written Comment - 성의없는 주석**
5. **Commented-Out Code - 주석으로 처리된 코드**

## Environments
1. **Build Requires More Than One Step - 여러 단계로 빌드해야한다.**
   * 한 단계로 끝나도록 , 간단하게 .. 한 명령으로 빌드
2. **Tests Require More Than One Step - 여러 단계로 테스트**
   * 모든 테스트는 한 명령으로, 아무리 열악해소 cli 명령어 하나로 가능해야한다. 

## Functions
1. **Too Many Arguments**
2. **Output Arguments - 출력인수**
3. **Flag Arguments - 플래그 인수**
   * 함수가 여러 기능을 한다는 뜻 
4. **Dead Function**
   * 아무도 호출하지 않는 함수는 삭제

## General
1. **Multiple Languages in One Source File**
2. **Obvious Behavior Is Unimplemented - 당연한 동작을 구현하지 않는 것**
3. **Incorrect Behavior at the Boundaries - 경계를 올바르게 처리하지 않는 것**
4. **Overridden Safeties - 안전 절차 무시 - warning을 끄고 무시하는 것**
5. **Duplication**
6. **Code at Wrong Level of Abstraction - 추상화 수준이 올바르지 못한 것**
   * 추상화로 개념을 분리할때는 철저히, 모든 저차원 개념을 파생클래스에 고차원 개념을 기초클래스에 넣는다.
7. **Base Classes Depending on Their Derivatives**
   *  기초 클래스가 파생클래스를 사용하면 문제가 있는 것
   *  기초 클래스와 파생 클래스를 나누는 가장 흔한 이유가 고차원 기초 클래스 개념을 저차원 파생 클래스 개념으로부터 분리해 독립성을 보장하기 위해서니
   *  기초 클래스는 파생 클래스를 아예 몰라야한다.
   *  예외로 파생 클래스 개수가 확실히 고정되어있으면 기초에서 파생클래스를 선택하는 코드가 들어간다.
   *  FSM 구현에서 많이 본 사례 - Finite State Machine
8. **Too Much Information**
   * 잘 정의된 인터페이스는 많은 함수를 제공하지 않는다. 결합도가 낮다.
   * 클래스가 제공하는 메서드는 작을수록 좋다.
   * 함수가 아는 변수고 작을 수록 좋다. 인스턴스 변수 수도 작을수록 좋다.
   * 자료, 유틸리티 함수, 상수, 임시변수를 숨기고 메서드나 인스턴스가 넘치는 클래스는 피해라
9. **Dead Code**
10. **Vertical Separation**
    * 사용되는 위치에 가깝게 정의한다.
    * 비공개 함수는 처음으로 사용한 직후 정의
11. **Inconsistency 일관성 부족**
12. **Clutter - 잡동사니**
    * 비어있는 기본 생성자? 쓸데없이 코드만 복잡하게 한다. 아무도 사용하지 않는 변수, 함수, 주석 등 제거!
13. **Artificial Coupling - 인위적 결합**
    * 서로 무관한 개념을 인위적으로 결합하지 않는다.
    * enum은 특정 클래스에 속할 이유가 없다.
    * 범용 static 함수도 마찬가지
14. **Feature Envy - 기능 욕심**
    * 클래스 메서드는 자기 클래스의 변수와 함수에 관심을 가져야지 다른 클래스의 변수와 함수에 관심을 가지면 안된다.
    * 메서드가 다른 객체의 참조와 변경자로 내용을 조작하면 그 객체 클래스 범위를 욕심내는 것 
    * ```java
      public class HourlyPayCalculator {
        public Money calculateWeeklyPay(HourlyEmployee e) {
        int tenthRate = e.getTenthRate().getPennies();
        int tenthsWorked = e.getTenthsWorked();
        int straightTime = Math.min(400, tenthsWorked);
        int overTime = Math.max(0, tenthsWorked - straightTime); 
        int straightPay = straightTime * tenthRate;
        int overtimePay = (int)Math.round(overTime*tenthRate*1.5);
        return new Money(straightPay + overtimePay); 
        }
      }
      ```
    * calculateWeeklyPay 은 HourlyEmployee 클래스의 범위를 욕심낸다.
    * 그럼 거기에 넣어야하는건가? 아니면 클래스를 하나 만들라는건가.
    * ```java
       public class HourlyEmployeeReport { 
        private HourlyEmployee employee ;
        public HourlyEmployeeReport(HourlyEmployee e) { 
          this.employee = e;
        }
        String reportHours() { 
          return String.format(
            "Name: %s\tHours:%d.%1d\n", employee.getName(), employee.getTenthsWorked()/10, employee.getTenthsWorked()%10);
        } 
      }
      ```
    * reportHours 가 HourlyEmployee 을 욕심내긴 하지만 HourlyEmployee가 보고서 형식을 알 필요가 없으니.. 절로 옮기면 위반
    * HourlyEmployee가 보고서 형식과 결합되므로 보고서 형식이 바뀌면 클래스도 바뀐다.
15. **Selector Arguments - 선택자 인수**
    *  목적을 기억하기 어렵고, 여러함수를 하나로 조합한다.
    *  큰 함수를 작은 여럿으로 쪼개지 않으려는 게으름의 소산이다.
    *  ```java
        public int calculateWeeklyPay(boolean overtime) {
          int tenthRate = getTenthRate();
          int tenthsWorked = getTenthsWorked();
          int straightTime = Math.min(400, tenthsWorked);
          int overTime = Math.max(0, tenthsWorked - straightTime); 
          int straightPay = straightTime * tenthRate;
          double overtimeRate = overtime ? 1.5 : 1.0 * tenthRate; 
          int overtimePay = (int)Math.round(overTime*overtimeRate); 
          return straightPay + overtimePay;
        }
       ```
    *  1.5배로 지급하면 true고, 아니면 false임...
    *  ```java
        public int straightPay() {
          return getTenthsWorked() * getTenthRate();
        }

        public int overTimePay() {
          int overTimeTenths = Math.max(0, getTenthsWorked() - 400); int overTimePay = overTimeBonus(overTimeTenths);
          return straightPay() + overTimePay;
        }

        private int overTimeBonus(int overTimeTenths) {
          double bonus = 0.5 * getTenthRate() * overTimeTenths; 
          return (int) Math.round(bonus);
        }

       ```
    * 부울 인수 뿐만 아니라 enum, int 등 함수 동작을 제어하려하는 인수는 다 바람직하지 않다.
    * 인수를 넘겨 동작하는 대신 새로운 함수를 만드는게 낫다.
16. **Obscured Intent - 모호한 의도**
17. **Misplaced Responsibility- 잘못 지운 책임**
    * 코드의 배치?
    * 직원이 근무한 총 시간을 보고서로 출력하는 함수
      * 보고서를 출력하는 함수에서 총 계를 계산하는 방법
      * 근무 시간을 입력 받는 코드에서 총계를 보관하는 방법
    * 성능때문에 입력 받는 모듈에서 총계를 계산하는 편이 좋다고 판단할 수 있다.
    * 이를 반영해서 함수명을 제대로 지어야한다.
    * 예를들어 근무시간을 입력 받는 모듈에 `computeRunningTotalOfHours` 를 만든다.
18. **Inappropriate Static-부적절한 static함수**
    * 언뜻보면 static함수로 해도 될것 같지만, 재정의할 가능성이 있으면 X
    * 조금이라도 의심스러우면 인스턴스 함수로 정의한다.
19. **Use Explanatory Variables-서술적 변수**
    * 서술적인 변수 이름은 많이 써도 좋다.
    * 계산을 여러 단계로 나누고, 중간값으로 서술적인 변수를 사용하면 좋다.
20. **Function Names Should Say What They Do-이름과 기능이 일치하는 함수**
    * addDay  / daysSince ~ 
21. **Understand the Algorithm - 알고리즘을 이해하라**
22. **Make Logical Dependencies Physical - 논리적 의존성을 물리적으로 드러내라**
    * 상대 모듈에 대해 뭔가 가정하면 안된다. - 논리적으로 의존
    * 의존하는 모든 정보를 명시적으로 요청하는게 낫다.
    * ```java
      public class HourlyReporter {
        private HourlyReportFormatter formatter; 
        private List<LineItem> page;
        private final int PAGE_SIZE = 55;

        public HourlyReporter(HourlyReportFormatter formatter) { 
          this.formatter = formatter;
          page = new ArrayList<LineItem>();
        }
        public void generateReport(List<HourlyEmployee> employees) { 
          for (HourlyEmployee e : employees) { 
            addLineItemToPage(e);
            if (page.size() == PAGE_SIZE)
              printAndClearItemList(); 
          }
          if (page.size() > 0) printAndClearItemList();
        }
        private void printAndClearItemList() { 
          formatter.format(page); 
          page.clear();
        }
        private void addLineItemToPage(HourlyEmployee e) { 
          LineItem item = new LineItem();
          item.name = e.getName();
          item.hours = e.getTenthsWorked() / 10;
          item.tenths = e.getTenthsWorked() % 10;
          page.add(item); 
        }
          public class LineItem { 
            public String name;
            public int hours;
            public int tenths;
          } 
        }
      ```
      * 근무시간 보고서를 가공되지 않은 상태로 출력하는 함수
      * HourlyReporter는 모든 정보를 모아 HourlyReportFormatter에 넘겨준다.
      * HourlyReportFormatter는 넘어온 정보를 출력한다.
      * PAGE_SIZE라는 상수에 논리적인 의존성이 있다.
      * 어째서 HourlyReporter 클래스가 페이지 크기를 알아야하는가? 이건 HourlyReportFormatter얘가 책임질 정보다.
      * 애초에 HourlyReporter가 페이지 크기를 알거라고 가정함, HourlyReportFormatter구현 중 하나가 페이지 크기 55를 제대로 처리하지 못하면 오류가 생긴다.
      * getMaxPageSize() 를 추가하면 논리적 의존성이 물리적 의존성으로 변한다.
23. **Prefer Polymorphism to If/Else or Switch/Case**
    * 3장을 떠올리면 의아하다? 새 유형을 추가할 확률보다 새 함수를 추가할 확률이 높은 코드에서는 switch 더 적합하다 주장함
    * switch선택보다 다형성을 먼저 고려해라
    * 유형보다 함수가 더 쉽게 변하는 경우는 드물다, 모든 switch문을 의심해라
    * switch문은 하나 버칙!
24. **Follow Standard Conventions - 표준 표기법을 따르라**
    * 팀이 정한 표준은 팀원 모두가 따라야한다. 실제 괄호를 넣는 위치는 중요하지않다.
    * 모두가 동의한 위치에 넣는다는 것이 중요하다.
    * 이 사실을 이해할 정도로 팀원들이 성숙해야한다.
25. **Replace Magic Numbers with Named Constants - 매직넘버는 명명된 상수로 변경**
26. **Be Precise - 정확해라**
    * 첫 번째 결과만 유일한 결과로 간주하는 것은 순진하다
    * 부동소수점으로 통화를 표현하는 행동은 거의 범죄다.
    * 갱신 가능성이 희박하다고 잠금과 트랜잭션 관리를 건너뛰는 행동은 게으름이다.
    * List로 선언할 변수를 ArrayList 선언하는 것은 지나친 제약이다.
27. **Structure over Convention - 관례보다 구조**
    * enum변수가 멋진 switch/case 문보다 추상 메서드가 있는 기초 클래스가 더 좋다.
    * 파생클래스는 추상 메서드를 모두 구현하지 않으면 안되니까 . 
28. **Encapsulate Conditionals -조건을 캡슐화 해라**
    * 부울 논리는 이해하기 어렵다.
29. **Avoid Negative Conditionals - 부정조건은 피해라**
    * 이해하기 어려움 긍정보다.
30. **Functions Should Do One Thing - 함수는 한 가지만 해야한다.**
    * ```java
       public void pay() {
        for (Employee e : employees) {
          if (e.isPayday()) {
            Money pay = e.calculatePay(); e.deliverPay(pay);
          } 
        }
      }
      ```
    * 루프를 돌고, 각 직원의 월급을 확인하고, 지급한다 - 세가지일을함
    * ```java
       public void pay() {
        for (Employee e : employees)
          payIfNecessary(e); 
        }
        private void payIfNecessary(Employee e) { 
          if (e.isPayday())
            calculateAndDeliverPay(e); 
        }
        private void calculateAndDeliverPay(Employee e) { 
          Money pay = e.calculatePay(); 
          e.deliverPay(pay);
        }
      ```
31. **Hidden Temporal Couplings - 숨겨진 시간적 결합**
    * 시간적 결합이 있을 수 있으나 숨겨선 안된다.
    * 일종의 연결 소자를 생성해 결합을 노출한다. 그럼 순서를 바꿔 호출할 수 없다.
32. **Don’t Be Arbitrary 일관성을 유지해라**
    * 구조에 일관성이 없으면 남들이 해치려고한다.
    * ```java
      public class AliasLinkWidget extends ParentWidget {
        public static class VariableExpandingWidgetRoot { 
          ...
        ... 
      }
      ```
    * VariableExpandingWidgetRoot이 AliasLinkWidget에 속할 필요가 전혀 없다.
    * AliasLinkWidget와 무관한 클래스가 AliasLinkWidget, VariableExpandingWidgetRoot을 사용
    * 이들은 AliasLinkWidget을 알필요가 없다.
33. **Encapsulate Boundary Conditions- 경계조건은 캡슐화해라**
34. **Functions Should Descend Only One Level of Abstraction - 함수는 추상화수준을 한단계만 내려가야한다.**
    * ```java
      public String render() throws Exception {
        StringBuffer html = new StringBuffer("<hr"); 
        if(size > 0)
          html.append(" size=\"").append(size + 1).append("\""); 
        html.append(">");
        return html.toString(); }    
      ```
    * 추상화 수준이 최소 두개는 섞여있다. 
    * 첫째는 수평선의 크기 , 둘때는 HR태그 자체의 문법
    * 네개이상의 대시(-)를 감지해 HR로 변환한다. 대시가 많은수록 크기가 커진다.
    * ```java
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
    * hr태그의 생성, size변수의 해석과 형식 지정이 혼재된 추상화 수준이였다.
35. **Keep Configurable Data at High Levels- 설정 정보는 최상위 단계에 둬라**
36. **Avoid Transitive Navigation- 추이적 탐색을 피해라**
    * 일반적으로 한 모듈은 주변 모듈을 모를수록 좋다.
    * A가 B를 써도 B가 C를 써도 A가 C를 알 필요가 없다.
    * 디미터의 법칙 / Writing Shy Code
    * 내가 사용하는 모듈이 내게 필요한 서비스를 모두 제공해야한다. 원하는 메서드 찾느라 탐색할 필요가 없어야한다.
