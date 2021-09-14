주석은 언제나 실패를 의미한다.
코드가 그 자체로 모든 설명을 할 수 있다면 주석은 필요하지 않으리
주석을 달 때마다 자신에게 표현력이 없다는 사실을 푸념해야 마땅하다

### 주석은 나쁜 코드를 보완하지 못한다.
코드에 주석을 추가하는 일반적인 이유는 코드 품질이 나쁘기 때문이다. => 죄송합니다.

### 코드로 의도를 표현라!
```java
  if ((employee.flags & HOURLY_FLAG) && (employee.age > 65))

  if (employee.isEligibleForFullBenefits())
```

### 좋은 주석
정말 좋은 주석은 달지 않는 것이지만 그나마 글자 값을 하는 주석들

1. 법적인 주석
```java
  // Copyright (C) 2003, 2004, 2005 by Object Mentor, Inc. All right reserved.
```

2. 정보를 제공하는 주석
```java 
  // 테스트 중인 Responder 인스턴스를 반환한다.
  protected abstract Responder responderInstance();

  => responderBeingTested() 로 바꾸는 것이 좋다, 이러면 주석 필요 x
```

3. 의도를 설명하는 주석
```java
  public int compareTo(Object o) {
    if(o instanceof WikiPagePath) {
      WikiPagePath p = (WikiPagePath) o;
      String compressedName = StringUtil.join(names, "");
      String compressedArgumentName = StringUtil.join(p.names, "");
      return compressedName.compareTo(compressedArgumentName);
    }
    return 1; // 오른쪽 유형이므로 정렬 순위가 더 높다
  }
```
4. 의미를 명료하게 밝히는 주석
5. 결과를 경고하는 주석
테스트 케이스를 실행할때 오래 걸리는 함수의 경우 주석으로 달아놓는 것은 좋은 방법,
요즘에는 @Ignore 속성을 이용해 테스트 케이스를 꺼버린다.

6. TODO 주석
```java
  // TODO-MdM 현재 필요하지 않다.
  // 체크아웃 모델을 도입하면 함수가 필요 없다
  protected VersionInfo makeVersion() throws Exception {
    return null;
  }
```

7. 중요성을 강조하는 주석

### 나쁜 주석

1. 주절거리는 주석
2. 같은 이야기를 중복하는 주석
  코드가 충분한 설명성을 갖추고 있어야 한다.
3. 오해할 여지가 있는 주석
4. 의무적으로 다는 주석
  => 이것과 같은 방식을 한때 선호했던 적이 있었다
5. 이력을 기록하는 주석
  예전에는 관례였다
6. 있으나 마나 한 주석
7. 무서운 잡음
8. 함수나 변수로 표현할 수 있다면 주석을 달지 마라
   ```java
    // 전역 목록 <smodule>에 속하는 모듈이 우리가 속한 하위 시스템에 의존하는가?
    if (smodule.getDependSubsystems().contains(subSysMod.getSubSystem()))


    ArrayList moduleDependers = smodule.getDependSubsystems();
    String ourSubSystem = subSysMod.getSubSystem();
    if (moduleDependees.contains(ourSubSystem))
   ```
9.  위치를 표시하는 주석
  소스 파일에서 특정 위치를 표시하려 주석을 사용하는 경우
10. 닫는 괄호에 다는 주석
11. 공로를 돌리거나 저자를 표시하는 주석
12. 주석으로 처리한 코드
  많이 남겨두고 있는 것 같다.
13. HTML 주석
14. 전역 정보
15. 너무 많은 정보
16. 모호한 관계
17. 함수 헤더
18. 비공개 코드에서 Javadocs
19. 예제