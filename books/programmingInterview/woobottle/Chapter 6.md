# 6. 트리와 그래프

```java
public abstract class Node {
  private Node[] children;

  public Node(Node[] children) {
    this.children = children;
  }

  public int getNumChildren() {
    return children.length;
  }

  public Node getChild(int index) {
    return children[index];
  }
}

public class IntNode extends Node {
  private int value;

  public IntNode(Node[] children, int value) {
    super(children);
    this.value = value;
  }

  public int getValue() {
    return value;
  }
}
```

### 이진 트리

```java
public class Ndoe {
  private Node left;
  private Node right;
  private int value;

  public Node(Node left, Node right, int value) {
    this.left = left;
    this.right = right;
    this.value = value;
  }

  public Node getLeft() { return left; }
  public Node getRight() { return right; }
  public int getValue() { return value; }
}
```

```python
class Node :
  def __init__(self, left=None, right=None, value):
    self.left = left
    self.right = right
    self.value = value

  def getLeft(self) :
    return self.left

  def getRight(self) :
    return self.right
  
  def getValue(self) :
    return self.value
```

```js
class Node {
  constructor(value, left = null, right = null) {
    this.left = left;
    this.right = right;
    this.value = value;
  }
  getLeft() {
    return this.left;
  }
  getRight() {
    return this.right;
  }
  getValue() {
    return this.value;
  }
}
```

### 이진 검색 트리
* 노드의 왼쪽 자식의 값이 반드시 자신의 값 이하이다.
* 노드의 오른쪽 자식의 값은 반드시 자신의 값 이상이다.

```
루트 노드에서 시작
현재 노드가 널이 아닌 동안 반복
  현재 노드의 값이 찾고자 하는 값이면
    현재 노드 리턴
  현재 노드의 값이 찾고자 하는 값보다 작으면
    오른쪽 자식을 현재 노드로 설정
  현재 노드의 값이 찾고자 하는 값보다 크면
    왼쪽 자식을 현재 노드로 설정
반복문 끝
```

재귀호출 형태
```java
Node findNode(Node root, int vlaue) {
  if (root == null) return null;
  int currval = root.getValue();
  if (currval == value) return root;
  if (currval < value) {
    return findNode(root.getRight(), value);
  } else {
    return findNode(root.getLeft(), value);
  }
}
```

### 힙
* 노드의 각 자식의 값은 노드 자신의 값 이하여야 한다 => 루트 노드의 값이 제일 크다.

### 일반적인 검색 방법

**너비 우선 검색**    
루트에서 시작하여 둘째 층을 왼쪽에서 오른쪽으로 훑어나가고, 그 다음 층을 또 왼쪽에서 오른쪽으로 훑어 나가는 방식, O(n),
큰 트리에 대해서는 하지 않는 것이 좋음, 모든 노드의 자식 노드를 저장해야 하기 때문에 메모리도 많이 사용한다.

**깊이 우선 검색**    
원하는 노드를 찾을 때까지, 끝에 다다를 때까지 쭉 내려가는 방식


### 종주
모든 노드를 방문하면서 각 노드에 대해 작업을 수행한다.   
* 프리오더 종주 => 노드 - 왼쪽노드 - 오른쪽 노드
* 인오더 종주 => 왼쪽노드 - 노드 - 오른쪽 노드
* 포스트오더 종주 => 왼쪽노드 - 오른쪽 노드 - 노드

### 그래프

자식이 딸린 노드로 구성된다.   
한 노드에 부모가 여럿이 있을수 있어서 루프(사이클)가 만들어질 수 있다.

### 트리 및 그래프 문제
1. 재귀 호출을 쓰지 않는 프리오더 종주
잘 보면 스택이여서 프리오더 지만 오른쪽 먼저 확인후에 값을 넣어준다.
```java
void preorderTraversal(Node root) {
  Stack<Node> stack = new Stack<Node>();
  stack.push(root);

  while (!stack.empty()) {
    Node curr = stack.pop();
    curr.printValue();
    Node n = curr.getRight();
    if (n != null) stack.push(n);
    n = curr.getLeft();
    if (n != null) stack.push(n);
  }
}
```

1. 가장 가까운 공통 조상

모든 값을 파악후에 찾고자 하는 값의 왼쪽과 오른쪽값의 사잇값 중 가장 낮은 값을 찾으면???
```
현재 노드 검사
value1과 value2가 모두 현재 노드의 값보다 작으면
  왼쪽 자식 검사
value1과 value2가 모두 현재 노드의 값보다 크면
  오른쪽 자식 검사
그렇지 않으면 
  현재 노드가 가장 가까운 공통 조상
```


```java
Node findLowestCommonAncestor(Node root, int value1, int value2) {
  while (root != null) {
    int value = root.getValue();

    if (value > value1 && value > value2) {
      root = value.getLeft();
    } else if (value < value1 && value < value2) {
      root = value.getRight();
    } else {
      return root;
    }
  }

  return null;
}
```

3. 이진 트리 힙 변환 
> 정렬되지 않은 이진 트리에 들어 있는 정수의 집합이 주어진다.   
> 배열 정렬 루틴을 써서 이 트리를 균형 이진 트리를 기반 자료구조로 하는 힙으로 변환하라.

=> 트리와 배열 자료구조를 서로 간에 변활할 수 있는 능력을 가늠하기 위한 것이다.

* 이진트리를 전위순회로 전부 배열에 넣고 이를 정렬한다. 정렬된 배열을 거꾸로 순회하여 트리의 루트노드로 하나씩 만든다???

배열로부터 균형 힙을 구축하는 데 있어서 핵심은 어떤 노드를 기준으로 그 자식의 상대적인 위치를 파악하는 일이다.
이진트리의 노드를 배열로 채울때   
루트는 0
루트의 자식은 1,2    
자식의 자식은 3,4, 5,6

부모의 인덱스 i, 자식의 인덱스 2i + 1, 2i + 2

다시 이렇게 배열로 된 트리를 힙으로 만들어야 함(최소힙 -> 부모가 자식보다 값이 항상 작은 힙, 최대힙 -> 부모가 자식보다 값이 항상 큰 힙)

```java
public static Node heapifyBinaryTree(Node root) {
  int size = traverse(root, 0, null); // 현재 노드 (전체 크기 가지고 오기 위한 코드)
  Node[] nodeArray = new Node[size];
  traverse(root, 0, nodeArray); // 노드를 배열로 넣음

  // Comparator 객체를 써서 값으로 노드 배열을 정렬함
  Arrays.sort(nodeArray, new Comparator<Node>(){
    @verride public int compare(Node m, Node n) {
      int mv = m.getValue(), nv = n.getValue();
      return ( mv < nv ? -1 : (mv == nv ? 0 : 1));
    }
  });

  for (int i =0;i<size; i++) {
    int left = 2*i + 1;
    int right = left + 1;
    nodeArray[i].setLeft(left >= size ? null : nodeArray[left]);
    nodeArray[i].setRight(right >= size ? null : nodeArray[right]);
  }
  return nodeArray[0];
}

public static int traverse(Node node, int count, Node[] arr) {
  if (node == null) 
    return count;
  if (arr != null)
    arr[count] = node;
  count++;
  count = traverse(node.getLeft(), count, arr);
  count = traverse(node.gerRight(), count, arr);
  return count;
}
```


4. 불균형 이진 검색 트리 

트리를 회전시켜 버린다. 개념이 이해가 잘 안갔었는데 좀 더 봐야겠다. 
핵심은 이와 같다. 

현재 노드의 왼쪽 자식이 이제 루트가 되고
왼쪽 자식의 오른쪽 노드가 현재 노드의 왼쪽 자식이 된다.
```
function swap(oldNode) {
  newNode = oldNode.left
  oldNode.left = newNode.right
  newNode.right = oldNode
}
```

### 요약
트리는 사이클이 없는 그래프이므로 결국은 그래프의 일종으로 볼 수 있다.
트리 문제 중에는 재귀 호출로 해결할 수 있는 게 많다.