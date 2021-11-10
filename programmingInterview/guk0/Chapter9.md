## 정렬 알고리즘
- 보통 언어에서는 퀵소트 정렬이 내장돼 있음
- 정렬 알고리즘을 선택할 시 고려할 사항
  - 정렬할 데이터 양
    - 데이터가 많을 때 최악의 경우 실행 시간이 크게 달라짐.
  - 데이터와 메모리
    - 데이터가 너무 많아 메모리에 다 올릴 수 없다면 조금 씩 잘라서 정렬하고 잘라진 각 조각을 합쳐 정렬된 데이터 모음을 만들어야 할 수도 있다.
  - 데이터가 정렬된 정도
    - 이미 정렬된 목록에 새 데이터를 추가할 때는 효율이 좋지만 정렬이 되지 않은 목록에 대해서 효율이 나쁜 알고리즘도 있다.
  - 필요한 추가 메모리의 양
    - 배열에 원소를 맞바꾸는 등의 방식으로 추가 메모리를 쓰지 않고 데이터를 정렬할 수 있는 알고리즘도 있음. 메모리가 여유롭지 않을 때 효율보다 추가 메모리를 적게 쓰는 점을 고려하여 알고리즘을 골라아 햘 수도.
  - 상대 위치 보존 여부
    - 정렬 면에서 볼 때 아무 상관없는 원소들의 상대적인 위치가 그대로 유지되는 알고리즘을 안정적인(stable) 알고리즘이라 부른다. 성능을 위해서 안정성을 희생해도 괜찮은 경우가 종종 있다.
- 표준 라이브러리의 정렬 알고리즘은 비교 알고리즘을 바탕으로 돌아간다.
  - 비교 알고리즘에서는 O(nlog(n))보다 빠른 알고리즘이 없다.


- 안정 정렬 
  - 정렬 후 같은 값의 요소의 순서가 보장
- 불안정 정렬
  - 정렬 후 같은 값의 요소의 순서 보장 x
- 내부 정렬
  - 정렬하고자 하는 모든 데이터가 메모리에 올라와 정렬이 수행되는 방식
- 외부 정렬
  - 정렬하고자 하는 데이터가 너무 크기 때문에 일부만 올려놓은 상태에서 정렬한 것을 다시 합하는 방식
- 제자리 정렬
  - 주어진 공간 외에 추가적인 공간을 사용하지 않는 정렬
<br>

### 선택 정렬
- 가장 단순한 정렬 알고리즘. 배열 전체를 훑으면서 **가장 작은 원소**를 찾아 첫 번째 원소와 위치 교환. 마지막 원소까지 반복.

```java
public static void selectionSortRecursive( int[] data ) {
  selectionSortRecursive(data, 0)
}

private static void selectionSortRecursive(int[] data, int start) {
  if (start < data.length - 1) {
    swap( data, start, findMinimumIndex(data, start) );
    selectionSortRecursive(data, start + 1)
  }
}

private static int findMinimumIndex( int[] data, int start ) {
  int minPos = start;

  for (int i = start + 1; i < data.length; ++i) {
    if (data[i] < data[minPos]) {
      minPos = i;
    }
  }
  return minPos;
}

private static void swap( int[] data, int index1, int index2 ) {
  if (index1 != index2) {
    int tmp = data[index1];
    data[index1] = data[index2];
    data[index2] = tmp;
  }
}
```
- 복잡도 : O(n(n-1) / 2) -> O(n^2)
- 데이터 원소를 움직이는게 비교 작업에 비해 느리다면 선택 정렬의 성능이 다른 알고리즘보다 좋을수도 있다.
- 알고리즘의 효율은 최적화 기준에 따라 달라질 수 있다.

<br>

### 삽입 정렬
- 한 번에 한 원소씩 이미 정렬된 다른 원소들과 비교하여 새 원소를 제 위치에 삽입하는 방식으로 정렬된 배열을 만든다.
- 가장 작은 원소를 찾는 선택정렬과 다르게 **인덱스 1**부터 시작하여 **앞의 원소들과 비교**한다.
```java
// 삽입 알고리즘으로 배열을 정렬하는 코드
public static void insertionSort(int[] data){
  for (i = 0; i < data.length; i++) {
    int tmp = data[i]
    for ( target = i + 1; target < data.length; target++ ) {      
      if (data[i] > target) {        
        data[i] = data[target];
        data[target] = tmp;
      } else {
        Break;
      }
    }
  }
}


public void insertionSort() {
    int[] array = this.array;
    int length = array.length;

    for (int i = 1; i < length; i++) {
        int j = i - 1;
        int key = array[i];
        while (j >= 0 && array[j] > key) {
            array[j + 1] = array[j];// element들을 하나씩 뒤로 미는 작업. 계속 index -1 의 값으로 바꿔줌.
            j--;// j가 -1까지 돈다.
        }
        array[j + 1] = key;
    }
    System.out.println(Arrays.toString(array));
}

```
- 리스트가 이미 정렬돼 있을 경우 O(n)의 효율.
- 정렬된 리스트에 새 원소를 추가 할때 매우 좋은 효율을 보임
- 평균 및 최악의 경우 O(n^2). 무작위로 정렬된 많은 데이터는 효율이 좋지 못함.

<br>

### 퀵 정렬
- 데이터 집합 내에서 한 피벗 값을 고른 후 피벗을 기준으로 집합을 두개로 나눠 왼쪽은 피벗 값보다 작은 값만, 오른쪽은 피벗보다 큰값만 넣는다.
- 더 이상 쪼갤 부분이 없을 때까지 각각의 부분집합에 대해 피벗/쪼개기 작업을 재귀적으로 적용.
- 병합정렬과의 차이
  - 병합정렬의 경우 하나의 리스트를 '절반'으로 나누어 분할 정복.
  - 퀵 정렬(Quick Sort)의 경우 피벗(pivot)의 값에 따라 피벗보다 작은 값을 갖는 부분리스트와 피벗보다 큰 값을 갖는 부분리스트의 크기가 다를 수 있다.

- 퀵 정렬은 데이터를 '비교'하면서 찾기 때문에 '비교 정렬'이다.
- 정렬의 대상이 되는 데이터 외에 추가적인 공간을 필요로 하지 않는다. - 제자리 정렬(in-place sort)
- 퀵 정렬은 병합정렬과는 다르게 하나의 피벗을 두고 두 개의 부분리스트를 만들 때 서로 떨어진 원소끼리 교환이 일어나기 때문에 불안정정렬(Unstable Sort) 알고리즘이기도 하다.
- O(n log(n)). 피벗을 인덱스 0으로 고르면 복잡도는 O(n^2)

```java
// swap이 없음.
public static void quickSortSimple( int[] data ) {
  if (data.length < 2) return;

  int pivotIndex = data.length / 2
  int pivotValue = data[pivotValue];
  int leftCount = 0;
  
  for (int i = 0; i < pivotIndex; ++i ) {
    ++leftCount;
  }
  // for (int i = 0; i < data.length; ++i) {
  // if (data[i] < pivotvalue>) ++leftCount;
  //  }

  int[] left = new int[leftCount];
  int[] right = new int[data.length - leftCount];
  int l = 0;
  int r = 0;
  // 부분집합 만들기.
  for (int i = 0; i < data.length; ++i) {
    if (i == pivotIndex) continue;

    int val = data[i];
    if (i < pivotIndex) {
      left[l++] = val;
    } else {
      right[r++] = val;
    }
  }


  quickSortSimple(left);
  quickSortSimple(right);

  System.arraycopy(left, 0, data, 0, left.length);
  data[left.length] = pivotValue;
  System.arraycopy(right, 0, data, left.length + 1, right.length);
}
```

``` java
public void quickSort(int left, int right) {
    int[] array = this.array;
    int pivot = array[(left + right) / 2];
    int leftPointer = left;
    int rightPointer = right;

    while (leftPointer <= rightPointer) {
        while (array[leftPointer] < pivot) leftPointer++;
        while (array[rightPointer] > pivot) rightPointer--;
        if (leftPointer <= rightPointer) swap(leftPointer++, rightPointer--);
    }

    if (left < rightPointer) quickSort(left, rightPointer);
    if (leftPointer < right) quickSort(leftPointer, right);

    System.out.println(Arrays.toString(array));
}

```

<br>

### 합치기 정렬(병합 정렬)
- 배열을 둘 이상의 부분집합으로 나누고 각 부분 집합을 정렬한 다음 부분집합을 다시 정렬된 형태로 합치는 방식을 사용하는 분할 정복형 알고리즘.

```java
// swap이 없음.
public static void mergeSortSimple( int[] data ) {
  if (data.length < 2) return;

  int mid = data.length / 2
  int[] left = new int[mid];
  int[] right = new int[data.length - mid];
  
  System.arraycopy(data, 0, left, 0, left.length);
  System.arraycopy(data, mid, right, 0, right.length);

  mergeSortSimple( left )
  mergeSortSimple( right )

  merge( data, left, right )
}

// 두 작은 배열을 하나의 큰배열로 합침.
private static void merge( int[] dest, int[] left, int[] right ) {
  int dind = 0;
  int lind = 0;
  int rind = 0;

  while( lind < left.length && rind < right.length ) {
    if (left[lind] <= right[rind]) {
      dest[dind++] = left[lind++];
    } else {
      dest[dind++] = right[rind++];
    }
  }

  // 아직 원소가 남은 배열에 있는 값을 복사.
  while( lind < left.length ) {
    dest[dind++] = left[lind++];
  }

  while( rind < right.length ) {
    dest[dind++] = right[rind++];
  }

}
```
- 혼합형 합치기 정렬 : 정해진 크기보다 작은 부분배열을 다른 알고리즘으로 정렬하는 방식.
  - 종료 조건을 다음과 같이 수정
  ```java
    if (data.length < 10) {
      insertionSort(data);
      return data;
    }
  ```
- 삽입 정렬은 합치기 정렬보다 오버헤드도 적고 데이터 집합이 작을 경우 효율적이므로 위와 같은 최적화 방법도 사용해볼 수 있다.
- 합치기 정렬은 데이터 집합이 메모리에 한번에 올리기에 너무 클 때 쓰기 좋은 방법.
- O(n log(n))

## 문제

### 안정적인 선택 정렬
> 안정적인 버전의 선택 정렬을 구현하라(같은 값의 요소의 순서가 보장)

- 선택 정렬의 삽입을 없애고 다른 방법으로 구현해야한다. swap과정이 반복되다보니 정렬되지 않은 키의 순서가 계속 바뀐다.
- 배열 삽입/삭제 작업을 해야하므로 O(1)연산(swap)에서 O(n)연산으로 바뀐다.
```java
public static void selectionSortStable(CursorableLinkedList data) {
  CursorableLinkedList.Cursor sortedBoundary = data.cursor(0);
  while (sortedBoundary.hasNext()) {
    sortedBoundary.add(
      getMinimum(data, sortedBoundary, nextIndex());
    )
  }
  sortedBoundary.close();
}

private Comparable getMinimum(CursorableLinkedList data, int start) {
  CursorableLinkedList.Cursor unsorted = data.cursor(start);
  CursorableLinkedList.Cursor minPos = data.cursor(start+1);
  Comparable minValue = (Comparable) minPos.previoud();

  while (unsorted.hasNext()) {
    if (((Comparable)unsorted.next()).comparableTo(minValue) < 0) {
      while (minPos.nextIndex() < unsorted.nextIndex()) {
        minValue = (Comparable) minPos.next();
      }

    }
  }

  minPos.remove();
  minPos.close();
  unsorted.close();
  return minValue;
}
```

<br/>

### 다중 키 정렬
> 직원에 대한 정보를 저장하기 위한 다음과 같은 객체로 이루어진 배열이 있다.
> public class Employee {
>   public String extension; 
>   public String givenname;
>   public String surname;
> }
> 표준 라이브러리의 정렬 루틴을 이용하여 회사 전화번호부처럼 성(surname) 알파벳순, 그리고 이름(givenname) 알파벳 순으로 정렬하라

- 성을 기준으로 정렬 후 이름순으로 정렬 -> 성을 먼저 비교한 다음 성이 같은 경우 이름을 비교.
- Comparator 라이브러리 사용.

```java
  import java.util.Comparator;

  public class EmployeeNameComparator implements Comparator<Employee> {
    public int compare(Employee e1, Employee e2) {
      int ret = e1.surname.compareToIgnoreCase(e2.surname);

      if (ret === 0) {
        ret = e1.givenname.compareToIgnoreCase(e2.givenname);
      }
      return ret;
    }
  }


  public static void sortEmployees(Employee[] employees){
    // 비교자 지정
    Arrays.sort(employees, new EmployeeNameComparator());
  }
```

<br/>

### 안정적인 정렬 코드

```java
public class EmployeesSequenceComparator implements Comparator<Employee> {
  public int compare(Employee e1, Employee e2) {
    int ret = e1.surname.compareToIgnoreCase(e2.surname);

    if (ret === 0) {
      ret = Integer.compare(e1.sequence, e2.givenname);
    }
    return ret;
  }
}

public static void sortEmployeesStable(Employee[] employees) {
  for (int i = 0; i < employees.length; ++i) {
    employees[i].sequence = i;
  }
  shakySort(employees, new EmployeesSequenceComparator());
}
```