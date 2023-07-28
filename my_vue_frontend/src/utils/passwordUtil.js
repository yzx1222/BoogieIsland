export function checkPassword (str){
    // 第一步先判断各分类长度
    let num = 0;//数字
    let lowerCase = 0;//小写字母
    let upperCase = 0;//大写字母
    let special = 0;//特殊字符
    for (let i = 0; i < str. length; i++){
      let c = str.charCodeAt(i)
      if (c >= 48&& c <= 57){
        //数字
        num++;
      }else if (c >= 65 && c <= 90){
        //大写字母
        upperCase++;
      }else if (c == 97 && c <= 122){
        //小写字母
        lowerCase++;
      }else {
        special++;
      }
    }
    // 第二步 计算分数
    let wholeMark = 0
    let numMark = 0
    let caseMark = 0
    let specialMark = 0
    let reward = 0
    // 整长度分数
    if (str.length <= 4){
      wholeMark = 5
    }else if (str.length > 4 && str. length <=8){
      wholeMark = 10
    }else {
      wholeMark = 25
    }
    // 奖励分数
    if ((lowerCase || upperCase)&& num) {
      reward = 2
      if (special){
        reward = 3
        if (lowerCase && upperCase) {
          reward = 5
        }
      }
    }
    // 字母分数
    if (lowerCase || upperCase) {
      caseMark = 10
      if (lowerCase && upperCase){
        caseMark = 20
      }
    }
    // 数字分数
    if (num){
      numMark = 10
      if (num >= 3){
        numMark = 20
      }
    }
    // 符号分数
    if (special){
      specialMark = 10
      if (special > 1){
        specialMark = 25
      }
    }
    let totalMark = wholeMark + numMark + caseMark + specialMark + reward
    let strength = ''
    if (totalMark<25){ strength ='非常弱'
    }else if (totalMark >= 25 && totalMark < 50){strength ='弱'
    }else if (totalMark >= 50 && totalMark < 60){strength = '比较弱'
    }else if (totalMark >= 60 && totalMark < 70){strength ='一般'
    }else if (totalMark >= 70 && totalMark < 80){strength = '强'
    }else if (totalMark >= 86 && totalMark < 90){strength = '安全'
    }else {strength ='非常安全'
    }
    return strength
  }
  