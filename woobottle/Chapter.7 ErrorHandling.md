# 7. ErrorHandling

### 오류 코드보다 예외를 사용하라

```java
  // 복잡한 예시
  public class DeviceController {
    ...
    public void sendShutDown() {
      DeviceHandle handle = getHandle(DEV1);
      // 디바이스 상태를 점검한다.
      if (handle != DeviceHandle.INVALID) {
        // 레코드 필드에 디바이스 상태를 저장한다.
        retriveDeviceRecord(handle);
        // 디바이스가 일시정지 상태가 아니라면 종료한다.
        if (record.getStatus() != DEVICE_SUSPENDED) {
          pauseDevice(handle);
          clearDeviceWorkQueue(handle);
          closeDevice(handle);
        } else {
          logger.log('Device suspended. Unable to shut down');
        }
      } else {
        logger.log('Invalid handle for: ' + DEV1.toString());
      }
    }
    ...
  }
```
위의 코드는 함수를 호출한 즉시 오류를 확인해야 하므로 복잡해진다.
그래서 오류를 발생하면 예외를 던지는 것이 낫다.

```java
  public class DeviceController {
    ...
    public void sendShutDown() {
      try {
        tryToShutDown();
      } catch (DeviceShutDownError e) {
        logger.log(e)
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
      throw new DeviceShutDownError("Invalid handle for :" + id.toString());
      ...
    }
    ...
  }
```

### Try-Catch-Finally 문부터 작성하라

```java
  public List<RecordedGrip> retrieveSection(String sectionName) {
    try {
      FileInputStream stream = new FileInputStream(sectionName);
      stream.close();
    } catch (FileNotFoundException e) { // 에러를 상세히 적어서 범위를 좁히자
      throw new StorageException("retrieval error", e);
    }
    return new ArrayList<RecordedGrip>();
  }
```

### 미확인(unchecked) 예외를 사용하라
확인된 예외가 뭐야??? => 확인 된 예외의 몇 가지 예는 IO 예외 및 FileNotFound 예외입니다

확인된 오류를 던진다면 함수는 선언부에 throws 절을 추가해야 한다.
대규모 라이브러리가 여러 함수를 연쇄적으로 호출하는 부분에서 
확인된 오류를 던지고 이에 대한 처리를 진행하고 있다면 
호출하는 모든 함수에서 확인된 오류에 대한 처리를 추가 해야한다.

### 예외에 의미를 제공하라
예외를 던질 때는 전후 상황을 충분히 덧붙인다.
오류 메시지에 정보를 담아 예외와 함께 던진다.

### 호출자를 고려해 예외 클래스를 정의하라

```java
  // 오류를 형편없이 분류한 사례
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
    ....
  }
```

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
  
  // LocalPort 클래스는 ACMEPort 클래스가 던지는 예외를 잡아 변환하는 Wrapper 클래스일 뿐이다
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
  }
```

외부 API를 사용할 때는 LocalPort 클래스처럼 감싸기 기법이 좋다. 
=> 외부 라이브러리와 프로그램 사이에 의존성이 줄어든다.
   나중에 다른 라이브러리로 갈아타도 비용이 적다
   감싸기 클래스에서 외부 API를 호출하는 대신 테스트 코드를 넣어주는 방법으로 프로그램을 테스트하기도 쉬워진다.
   특정업체가 API를 설계한 방식에 발목 잡히지 않는다.

프로그램 사이의 의존성의 기준은 무엇일까?
* 코드에서 두 모듈간의 연결
* 하나의 모듈이 변경되면 연결된 다른 모듈들도 변경된다

### 정상 흐름을 정의하라

```java
  // 비효율적 처리
  try {
    MealExpenses expenses = expensesReportDAO.getMeals(employee.getID());
    m_total += expenses.getTotal();
  } catch (MealExpensesNotFound e) {
    m_total += getMealPerDiem();
  }
  
  // 효율적 처리
  MealExpenses expenses = expenseReportDAO.getMeals(employee.getID());
  m_total += expenses.getTotal();

  public class PerDiemMealExpenses implements MealExpenses {
    public int getTotal() {
      // 기본값으로 일일 기본 식비를 반환한다
      // 청구를 했으면 청구 비용만큼 들어오겠네
    }
  }
```

### null을 반환하지 마라

```java
  List<Employee> employees = getEmployees();
  if (employees != null) {
    for(Employee e : employees) {
      totalPay += e.getPay();
    }
  }

  // getEmployee는 null을 반환할수도 있다.
  List<Employee> employees = getEmployees();
  for (Employee e : employees) {
    totalPay += e.getPay();
  }

  public List<Employee> getEmployees() {
    if (직원이 없다면) {
      return Collections.emptyList(); // 읽기 전용 리스트를 반환한다.
    }
  }
```

### null을 전달하지 마라

null을 전달했을때 NullPointerExceptin이 발생할수 있다. 
아래는 그 대안들

```java
  public class MetricsCalculator {
    public double xProjection(Point p1, Point p2) {
      if (p1 == null || p2 == null) {
        throw InvalidArgumentException(
          "Invalid argument for MetricsCalculator.xProjection"
        );
      }
      return (p2.x - p1.x) * 1.5;
    }
  }

  public class MetricsCalculator {
    public double xProjection(Point p1, Point p2) {
      assert p1 != null : "p1 should not be null";
      assert p2 != null : "p2 should not be null";
      return (p2.x - p1.x) * 1.5;
    }
  }
```

### 결론
오류처리를 프로그램 논리와 분리해 독자적인 사안으로 고려하면 튼튼하고 깨끗한 코드를 작성할 수 있다.
오류 처리를 프로그램 논리와 분리하면 독립적인 추론이 가능해지며 코드 유지보수성도 크게 높아진다.