

# Error Handling

* 뭔가 잘못될 가능성은 늘 존재한다. 
* 여기저기 흩어진 오류 처리 코드 때문에 더러워진다.
* 그래서 뭐 잘하라는 뜻

## Use Exceptions Rather Than Return Codes

```java
public class DeviceController { 
  ...
	public void sendShutDown() { 
    DeviceHandle handle = getHandle(DEV1); 
    // Check the state of the device
		if (handle != DeviceHandle.INVALID) {
			// Save the device status to the record field 
      retrieveDeviceRecord(handle);
			// If not suspended, shut down
			if (record.getStatus() != DEVICE_SUSPENDED) {
				pauseDevice(handle); 
        clearDeviceWorkQueue(handle); 
        closeDevice(handle);
			} else {
				logger.log("Device suspended. Unable to shut down");
			}
		} else {
			logger.log("Invalid handle for: " + DEV1.toString()); 
    }
  }
... 
}
```

* 함수를 호출한 즉시 오류를 확인해야하기 때문에 복잡해짐
* 잊기도 쉬움
* 오류 발생하면 예외를 던지는게 낫다. 그럼 호출자 코드가 더 깔끔해진다. 
* 논리가 오류 처리 코드와 뒤섞이지 않음

```java
public class DeviceController { 
  ...
	public void sendShutDown() { 
    try {
			tryToShutDown();
    } catch (DeviceShutDownError e) {
			logger.log(e); 
    }
	}
  private void tryToShutDown() throws DeviceShutDownError { 
    DeviceHandle handle = getHandle(DEV1);
		DeviceRecord record = retrieveDeviceRecord(handle);
		pauseDevice(handle); 
    clearDeviceWorkQueue(handle); 
    closeDevice(handle);
	}
	private DeviceHandle getHandle(DeviceID id) { 
    ...
			throw new DeviceShutDownError("Invalid handle for: " + id.toString());
		... 
  }
... 
}
```

* 깨끗하고, 품질도 나음
* 로직이 분리됨

## Write Your Try-Catch-Finally Statement First

* 트랜잭션하고 비슷하다. try에서 무슨 일이 생기든 catch블록은 프로그램 상태를 일관성 있게 유지해야한다.

* ```java
  @Test(expected = StorageException.class)
  public void retrieveSectionShouldThrowOnInvalidFileName() {
  	sectionStore.retrieveSection("invalid - file"); 
  }
  
  public List<RecordedGrip> retrieveSection(String sectionName) { 
    try {
  		FileInputStream stream = new FileInputStream(sectionName) 
  		stream.close();
    } catch (FileNotFoundException e) {
  			throw new StorageException("retrieval error", e); 
    }
  	return new ArrayList<RecordedGrip>(); 
  }
  ```

* 강제로 예외를 일으키는 테스트 케이스를 작성한 후 테스트를 통과하게 코드를 작성하는 방법

* 그럼 자연스럽게 try 블록의 트랜잭션 범위부터 구현하게 됨

## Use Unchecked Exceptions

* Checked Exception handling하는게 꼭 좋은건 아님 - OCP를 위반함
* 만약 예외 던졌는데 catch 블록이 세단계 위에있으면? 그 메서드 선언부를 고쳐야하자나, 그럼 모듈 다시빌드 그거
* 최상위 함수가 아래 함수를 호출, 그아래,, 그아래 , .. 최 하위 함수를 변경해 새로운 오류를 던진다고 가정하면. 선언부에 추가해야함
  1. catch 블록에서 새로운 예외를 처리하거나
  2. 선언부에 throw절을 추가
* 결과적으로 최하위에서 최상위까지 연쇄적인 수정 
* throws 경로에 위치하는 모든 함수가 최하위에서 던지는 예외를 알아야하므로 캡슐화가 깨짐
* 의존성이라는 비용이 이익보다 크다

## Provide Context with Exceptions

* 오류메시지에 정보를 담아 예외와 함께 던진다. 실패한 연산 이름과 실패 유형도 언급한다.
* catch 블록에서 오류를 기록하도록 충분한 정보를 넘겨준다.

## Define Exception Classes in Term of a Caller's Needs

* 오류가 발생한 위치로 분류가 가능하다.

* 유형으로 분류 가능

* ```java
  ACMEPort port = new ACMEPort(12);
  try { 
    port.open();
  } catch (DeviceResponseException e) { 
    reportPortError(e);
  	logger.log("Device response exception", e);
  } catch (ATM1212UnlockedException e) { 
    reportPortError(e); 
    logger.log("Unlock exception", e);
  } catch (GMXError e) { 
    reportPortError(e);
  	logger.log("Device response exception");
  } finally { 
    ...
  }
  ```

  * 외부 라이브러리가 던질 예외를 모두 잡아낸다.
  * 중복도 심하지만 - 오류 기록 / 수행 가능한지 확인 등 어차피 우리가 하는거랑 비슷해?

  ```java
  LocalPort port = new LocalPort(12); 
  try {
  	port.open();
  } catch (PortDeviceFailure e) {
  	reportError(e);
  	logger.log(e.getMessage(), e);
  } finally {
  	... 
  }
  ```

* ```java
  public class LocalPort { 
    private ACMEPort innerPort;
  	public LocalPort(int portNumber) { 
      innerPort = new ACMEPort(portNumber);
  	}
  	public void open() { 
      try {
  		  innerPort.open();
  	  } catch (DeviceResponseException e) {
    		throw new PortDeviceFailure(e);
      } catch (ATM1212UnlockedException e) {
        throw new PortDeviceFailure(e);
  	  } catch (GMXError e) {
        throw new PortDeviceFailure(e);
  		} 
    }
  ... 
  }
  ```

* LocalPort 처럼 ACMEPort 를 감싸는 클래스는 매우 유용

* 외부 API를 쓸때는 wrapping하는게 최선이다. 그럼 의존성이 줄어든다. 다른 라이브러리로 갈아타도 비용이 적다.

* 테스트코드를 넣어줘서 테스트도 쉬워짐

* API설계한 방식에 발목 잡히지 않는다.

## Define the Normal Flow

* 때론 중단이 적합하지 않을 때가있다.

* ```java
  try {
  	MealExpenses expenses = expenseReportDAO.getMeals(employee.getID()); 
  	m_total += expenses.getTotal();
  } catch(MealExpensesNotFound e) { 
  	m_total += getMealPerDiem();
  }
  ```

* 식비를 비용으로 청구 안했으면 기본 식디를 총계에 더한다.

* 예외가 논리를 따라가기 어렵게 만든다.

```java
MealExpenses expenses = expenseReportDAO.getMeals(employee.getID()); m_total += expenses.getTotal();
```

* ExpenseReportDAO를 고쳐 MealExpense만 반환,  `getTotal` 을 고쳐 기본값으로
* 클래스를 만들거나 객초를 조작해 특수한 사례를 처리, 
* 클라가 처리 X
* 클래스나 객체가 캡슐화해서 처리
* Special Case Pattern이라고 부른다.

## Don't Return Null

```java
public void registerItem(Item item) { 
	if (item != null) {
		ItemRegistry registry = peristentStore.getItemRegistry(); 
		if (registry != null) {
			Item existing = registry.getItem(item.getID());
			if (existing.getBillingPeriod().hasRetailOwner()) {
				existing.register(item); 
      }
		} 
  }
}
```

* 호출자에게 떠넘기는거임
* `peristentStore` 은 널체크 안하니까 nullpointerexception임 
* 위든 어디든 어디서 처리하는거일지도 모르는데 무튼 나쁨
* 결국 null 체크가 넘 많아서 문제

```java
List<Employee> employees = getEmployees(); 
if (employees != null) {
	for(Employee e : employees) { 
    totalPay += e.getPay();
	} 
}
```

* 그냥 빈 배열 리턴하면 

```java
List<Employee> employees = getEmployees(); 
for(Employee e : employees) {
	totalPay += e.getPay(); 
}
```



## Don't Pass Null

* 정상적인 인수로 Null을 기대하는게 아니라면,... 넘기지마

* ```java
  public class MetricsCalculator {
  	public double xProjection(Point p1, Point p2) { 
  	return (p2.x – p1.x) * 1.5;
  	}
  ... 
  }
  ```

* 만약 null넘기면 에러

* ```java
  public double xProjection(Point p1, Point p2) { 
    if(p1==null||p2==null){
  		throw InvalidArgumentException("Invalid argument for MetricsCalculator.xProjection");
  	}
  	return (p2.x – p1.x) * 1.5; 
  }
  ```

* 쪼끔 더 나을진 몰라도 어쨋든 InvalideArgumentException을 잡아내야함

* ```java
  public class MetricsCalculator {
  	public double xProjection(Point p1, Point p2) { 
  		assert p1 != null : "p1 should not be null"; 
  		assert p2 != null : "p2 should not be null"; 
  		return (p2.x – p1.x) * 1.5;
  	} 
    }
  
  ```

* 읽기는 편하지만 해결은 안된다. 어쨋든 에러발생함

* 애초에 못보내게 만드는 정책이 합리적이다.

## 결론

* 깨끗한 코드는 읽기 좋아야한다. 하지만 안정성도 높아야함.
* 이 둘은 상충하는 목표가 아니다.
* 오류 처리를 프로그램 논리와 분리해 독자적인 사안으로 고려하면 튼튼하고 깨끗한 코드를 작성할 수 있다.
* 독립적인 추론이 가능하고 유지보수성도 크게 높아진다.
* 







