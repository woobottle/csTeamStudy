### 작게 만들어라
```java
  public static String renderPageWithSetupsAndTeardowns (
    PageData pageData, boolean isSuite
   ) throws Exception {
     boolean isTestPage = pageData.hasAttribute("Test");
     if (isTestPage) {
       WikiPage tesetPage = pageData.getWikiPage();
       StringBuffer newPageContent = new StringBuffer();
       includeSetupPages(testPage, newPageContent, isSuite);
       newPageContent.append(pageData.getContent());
       includeTeardownPages(testPage, newPageContent, isSuite);
       pageData.setContent(newPageContent.toString());
     }
     return pageData.getHtml();
   }
```

아래의 함수는 위의 함수를 리팩토링 한것.

```java
  public static String renderPageWithSetupsAndTearDowns ( PageData pageData, boolean isSuite ) throws Exception {
    if (isTestPage(pageData)) {
      includeSetupAndTeardownPages(pageData, isSuite);
    }
    return pageData.getHtml();
  } 
```

함수에서 들여쓰기 수준은 1단이나 2단을 넘어서면 안된다. 그만큼 함수가 커져서는 안된다.

### 한 가지만 해라!

지정된 함수 이름 아래에서 추상화 수준이 하나인 단계만 수행한다면 그 함수는 한 가지 작업만 한다 -> 결국 이름 짓기 싸움인듯 (약간 애매하다는 개인적인 생각)

### 함수 당 추상화 수준은 하나로!
함수가 확실히 '한 가지' 작업만 하려면 함수 내 모든 문장의 추상화 수준이 동일해야 한다. 

추상화 수준 높다 -> getHtml()
추상화 수준 중간 -> String pagePathName = PathParser.render(pagepath);
추상화 수준 낮다 -> .append("/n")

1. 위에서 아래로 코드 읽기: <strong>내려가기 규칙</strong>
   1. 위에서 아래로 이야기처럼 읽혀야 좋다. 한 함수 다음에는 추상화 수준이 한 단계 낮은 함수가 온다(**)

### Switch 문
   1. switch 문을 다형성 객체를 생성하는 코드 안에서만 사용한다. 이렇게 상속 관계로 숨긴 후에는 절대로 다른 코드에 노출하지 않는다. -> switch문을 사용하면서 규칙을 가지고 사용해본적은 없는것 같다.
      ```java
        public abstract class Employee {
          public abstract boolean isPayday();
          public abstract Money calculatePay();
          public abstract void deliverPay(Money pay);
        }

        ---------------------------------

        public interface EmployeeFactory {
          public Empoyee makeEmployee(EmployeeRecord r) throws InvalidEmployeeType;
        }

        ----------------------------------

        public class EmployeeFactoryImpl implements EmployeeFactory {
          public Emloyee makeEmployee(EmployeeRecord r) throws InvalidEmployeeType {
            switch (r.type) {
              case COMISSIONED:
                return new CommissionedEmployee(r);
              case HOURLY:
                return new HourlyEmployee(r);
              case SALARIED:
                return new SalriedEmployee(r);
              default:
                throw new InvalidEmployeeType(r.type);
            }
          }
        }
      ```

### 서술적인 이름을 사용하라!
의미있는 이름 짓는 부분에서 나오는 내용들

### 함수 인수
인수는 적을수록 좋다.
4개 이상은 특별한 이유가 필요하다. 특별한 이유가 있어도 사용하면 안된다. -> 생각없이 사용했던 적이 많은것 같다.
includeSetupPageInto(newPageContent)는 함수 이름과 인수 사이에 추상화 수준이 다르다(**) -> 이 정도까지 감안하는 실력이 되고싶다. 내가보기엔 높다(낮다) 인듯????

  1. 많이 쓰는 단항 형식
    1. 함수에 인수 1개를 넘기는 가장 흔한 두가지 경우
    ```java
      // 인수에 질문을 던지는 경우
      boolean fileExists("MyFile")

      // 인수를 뭔가로 변환해 결과를 반환하는 경우
      InputStream fileOpen("MyFile") // String 형의 파일 이름을 InputStream으로 변환한다.
    ```
  2. 플래그 인수
     1. 절대 지양하자. (이전에 그레이토터스의 경우)
  3. 이항 함수
     1. 직교좌표계 같은 함수는 예외
  4. 삼항 함수
     1. 피하자
  5. 인수 객체
     1. Circle makeCircle(double x, double y, double radius) => Circle makeCircle(Point center, double radius)
      x,y를 묶어서 표현하게 되므로 개념을 표현하게 된다.
  6. 동사와 키워드
     1. assertEquals < assertExpectedEqualsActual(expected, actual) => 인수 순서를 기억할 필요가 없어진다

### 부수 효과를 일으키지 마라!

### 명령과 조회를 분리하라!
함수는 뭔가를 수행하거나 뭔가에 답하거나 둘중 하나만 해야 한다.

### 오류 코드보다 예외를 사용하라!
명령함수에서 오류코드를 반환하고 이를 오류 코드와 비교하는 것은 if문의 중첩을 가져올수 있다. 
예외처리로 이용하는 것이 좋다
```java
  if (deletePage(page) == E_OK) {
    if (registry.deleteReference(page.name) == E_OK) {
      if (configKeys.deleteKey(page.name.makeKey()) == E_OK) {
        logger.log("page deleted");
      } else {
        logger.log("configKey not deleted")
      }
    } else {
      logger.log("deleteReference from registry failed")
    } else {
      logger.log("delete failed");
      return E_ERROR;
    }
  }

  try {
    deletePage(page);
    registry.deleteReference(page.name);
    configKeys.deleteKey(page.name.makeKey())
  } catch (Exception e) {
    logger.log(e);
  }
```

### Try/Catch 블록 뽑아내기
try/catch 블록은 원래 추하다 => 요새 백엔드에 엄청 쓰고 있는데 추하다니....
try/catch 블록을 별도 함수로 뽑아내는 편이 좋다
```java
  public void delete(Page page) {
    try {
      deletePageAndAllReferences(page);
    } catch (Exception e) {
      logError(e);
    }
  }
```

### 반복하지 마라

### 구조적 프로그래밍
함수는 return 문이 하나여야 한다. => 이제까지 사용하던 방식이랑 전혀 반대되는 방식이다.
하지만 함수가 작다면 위 규칙은 별 이익을 제공하지 못한다.

### 함수를 어떻게 짜죠?
처음에는 길고 복잡하게, 중복된 루프도 많다.
점점 다듬어 들어간다. 
최종적으로는 이 장에서 설명한 규칙에 부합하는 함수가 만들어 진다.