# 信息管理子系统内部说明

## 数据词典基本说明

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
### 学生用户
#### Class

```java
public Class Student {
  private char[10]    id;
  private char[11]    contact;
  private String      name;
  private Gender      gender;      // Enumeration

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
public Class Teacher {
  private char[10]  id;
  private char[11]  contact;
  private String    name;
  private Gender    gender;      // Enumeration

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

### 课程信息
#### Class

```java
public Class Course {
  public Class TimeAndRoom {
    ClassTime time;
    Classroom room;
  }

  private char[8]                                   id;
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
