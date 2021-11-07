def solution(sentence) :
  listed = sentence
  result = []

  def get_all_list(elements, start) :
    for i in range(start, len(sentence)) :
      print(elements, i)
      elements.append(listed[i])
      result.append("".join(elements[:]))
      if i < len(listed) :
        get_all_list(elements, i + 1)
      elements.pop()
    
  get_all_list([], 0);
  return result


print(solution('wxyz'))