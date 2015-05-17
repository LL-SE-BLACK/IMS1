# 信息管理子系统内部说明
## 数据流基本说明

![data stream](./datastream.png)

|       数据流名     |     来源     |     去向     |                                   说明                                       |
| ------------------ | ------------ | ------------ | ---------------------------------------------------------------------------- |
| 学生用户指令       | 学生用户     | 教学管理系统 | 包括学生用户发出的登陆指令，成绩查询指令，课程信息查询指令，教室查询指令等等 |
| 学生指令执行结果   | 教学服务系统 | 学生用户     | 教务系统呈现给用户的数据                                                     |
| 教师用户指令       | 教师用户     | 教学管理系统 | 包括教师用户发出的登陆指令，课程查询指令，教室查询指令，学生成绩录入信息等等 |
| 教师指令执行结果   | 教学服务系统 | 教师用户     | 教务系统呈现给用户的数据                                                     |
| 管理员用户指令     | 管理员用户   | 教学管理系统 | 包括管理员用户发出的修改学生选课信息，成绩信息等指令                         |
| 管理员指令执行结果 | 教学服务系统 | 管理员用户   | 教务系统呈现给用户的数据                                                     |

## 数据元素&精度基本说明

|    数据名   |        类型定义       |   字节   |                说明              |                示例              |
| ----------- | --------------------- | --------:| -------------------------------- | --------------------------------:|
| name        | varchar(20)           | 20       | 姓名，最多20个字母或10个汉字组成 | 董可扬                           |
| student_id  | char(10)              | 10       | 学生学号，由十位数字组成         | 3120102084                       |
| teacher_id  | char(6)               | 6        | 教职工工号，由6位数字组成        | 123456                           |
| contact     | char(11)              | 11       | 联系方式，由11位数字组成的手机号 | 18868107127                      |
| password    | char(32)              | 32       | md5校验产生的密文32位字符串密文  | 1055d3e698d289f2af8663725127bd4b |
| grade       | integer(1897, 9999)   | 4        | 年级，用入学年份表示             | 2012                             |
| score       | integer(0, 100)       | 4        | 学生课程得分                     | 95                               |
| credit      | integer(0, INFINITY)  | 4        | 课程学分或学生获得学分           | 4.5                              |
| course_name | varchar(110)          | [0, 110] | 课程名称，由汉字、字母和数字组成 | 软件工程                         |
| course_id   | char(8)               | 8        | 课程编号，由8个字母或数字组成    | 21120261                         |
| classroom   | varchar(50)           | [0, 50]  | 教室名称，由建筑名称和门牌号构成 | 曹光彪二期101                    |

## CRC说明
### 登录
#### Class

```java
class Login {
  private char[]    id;
  private char[]    password;  // char[32] for md5 password
  private LoginType type;      // Enumeration
}
```

#### Responsibility
- 记录登录时的id，并通过登录类型验证id长度
- 对比md5加密后的密码和数据库中存储的密码
- 验证登录信息成功后返回反馈信息
- 验证失败后请用户重新输入，超过一定次数则拒绝继续尝试

#### Collaborator
- __INNER__ 通过验证后创建用户实例
- __OUTER__ _TODO_

### 基本用户
#### Class

```java
public class User {
  private char[]  id;       // char[10] for Student, char[6] for Teacher
  private char[]  contact;  // char[11]
  private String  name;
  private Gender  gender;   // Enumeration
}
```

### 学生用户
#### Class

```java
public class Student extends User {
  private College     college;     // Enumeration
  private Major       major;       // Enmueration
  private Grade       grade;       // Enmueration
  private int         gpa;
  private int         credits;

  private Schedule    schedule;    // Structure Reference
  private Transcript  transcript;  // Structure Reference
}
```

#### Responsibility
- 记录学生的基本信息，包括三个部分
  - 姓名、学号、联系方式、性别基本信息
  - 学院、专业、年级、成绩、学分学业信息
  - 课表、成绩单外部结构信息
- 通过外部引用记录学生的课表、成绩单信息
- 提供对学生个人信息的查询服务

#### Collaborator
- __INNER__ 学生用户通过登录接口输入用户id和加密后的密码，通过验证后登录成功，即创建该学生用户的`Student`类实例；由于密码只在登录时用到，因此类内不包含密码属性
- __OUTER__ _TODO_

### 教职工用户
#### Class

```java
public class Teacher extends User {
  private College   college;     // Enumeration
  private Major     major;       // Enmueration
  private Degree    degree;      // Enumeration
  private Title     title;       // Enumeration

  private Schedule  schedule;    // Structure Reference
}
```

#### Responsibility
- 记录教职工的基本信息，包括三个部分
  - 姓名、工号、性别、联系方式基本信息
  - 学院、专业、学位、职称工作信息
  - 课表结构信息
- 通过外部引用记录课表信息
- 提供对教职工个人信息的查询服务

#### Collaborator
- __INNER__ 教职工用户通过登录接口输入用户id和加密后的密码，通过验证后登录成功，即创建该用户的`Teacher`类实例；由于密码只在登录时用到，因此类内不包含密码属性
- __OUTER__ _TODO_

### 管理员
#### Class

```java
public class Administrator extends User {
  private Right rights;  // Structure Reference
}
```

#### Responsibility
- 记录管理员的基本信息和权限信息
- 提供对学生、教职工用户信息的修改服务
- 提供对系统信息（课表）等的修改服务

#### Collaborator
- __INNER__ 提供管理员用户修改系统数据、其他用户数据的服务
- __OUTER__ _TODO_


### 课程信息
#### Class

```java
public class Course {
  public Class TimeAndRoom {
    ClassTime time;
    Classroom room;
  }

  private char[]                                    id;
  private String                                    name;
  private int                                       credits;

  private Semester                                  semester;      // Enumeration
  private ArrryList<Classroom>                      examRoom;      // Structure Reference

  private ExamTime                                  examTime;      // Structure Reference
  private ArrayList<Teacher>                        teachers;      // Structure Reference
  private ArrayList<Course>                         requirements;  // Structure Reference
  private HashMap<Teacher, ArrayList<TimeAndRoom>>  classTimeAndRooms;
}
```

#### Responsibility
- 存储课程信息，包括
  - 课程名、课程编号、学分基本信息
  - 学期类型、考试教室信息
  - 考试时间、考试地点、任课老师、上课时间地点信息
- 与自动排课子系统进行交互
- 发送课程信息至自动排课子系统
- 接受来自排课系统的课程信息

#### Collaborator
- __INNER__ 提供课程信息的查询服务
- __OUTER__ _TODO_
