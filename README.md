# 约定

- 需要适配器实现的、表示参数的抽象类一般名为`IParams`；
- 提供增、删、查，以及改实体对象的抽象类一般叫做`IXXXRepository`，其中`XXX`为实体的类名；
- 用例有一个统一的入口`run`方法；
- 通过`run`的返回值和异常来告知外界一个用例的执行结果；

## Entity

- 每一个实体类的构造方法都是无参的；
- 每一个实体类都可以提供一个`new`方法，用于通过基本的要素构造出这个类的实例对象；
- 每一个实体类都有一个`id`属性。

## HTTP

- 凡是表示创建资源的含义的HTTP API，都应当返回201状态码，并在payload中返回所创建的资源的唯一标识。

## Interface

- 每一个接口的实现类都要在所实现的方法中添加type hints；
- 不同用例的输入参数不完全相同，因此建议在它们的类名中添加用例名作为前缀，例如`IRegistrationParams`和`ILoginParams`；
- Repository应当是对应于某一个Entity的，不随着用例的变化而变化，因此不需要区分`ILoginUserRepository`和`IRegistrationUserRepository`，统一为`IUserRepository`即可。