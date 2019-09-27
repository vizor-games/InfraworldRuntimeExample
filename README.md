# Vizor Infraworld exapmle

## Overview
Welcome to the **Infraworld Runtime** example project. The main goal of this tutorial is to show you how to get Infraworld sources, to generate *grpc/protobuf* and *protocol/transport* code using **Infraworld Protobuild** tool, to generate Unreal Engine friendly code with **Infraworld Cornestone** and finnaly how to connect all this stuff together to integrate **InfraworldRuntime** plugin into your UE project.


## Understanding Infraworld ecosystem

Infraworld is divided into three pieces:

- **[Infraworld Protobuild](https://github.com/vizor-games/infraworld-protobuild)** is an **optional** build tool helping you to keep your protobuf and gRPC wrapper code in a consistent state for all programming languages you're using across your projects.

- **[Infraworld Cornerstone](https://github.com/vizor-games/infraworld-cornerstone)** is an **optional** converter utility, used to generate UE4-friendly code to provide gRPC functionality into your game. 

- **[Infraworld Runtime](https://github.com/vizor-games/InfraworldRuntime)** - is a **required** library that enables Unreal Engine 4 to work with Google gRPC services using either C++ or Blueprints.

## Getting started

In this tutorial I want to show how to create a simple grpc server written in python which can handle two simple requests: `Hello(string name)` that takes a string and returns an other sting to the client like `Hello ${name}`. Second message `ServerTimeRequest` takes no arguments and returns server time structure like: 

```
struct
{
	int64 unixTimeStamp;
	uint32 hours;
	uint32 minutes;
	uint32 seconds;
	string timezone;
	string location;
}
```

Also you need to download **[InfraworldRuntime](https://github.com/vizor-games/InfraworldRuntime)** plugin. You can download precompiled binaries from the release page or clone and build the project by yourself. After this you have to copy the `InfraworldRuntime` plugin folder into `${InfraworldDemo}/Plugins`

### Protocol Buffers

First of all, you need at least one `.proto` file. Let's create a directory called `proto` for this. In `proto` directory create a file called `vizor_demonstration.proto`

Let's describe which requests we can send to the server and what do we expect to receive on the client: 

```protobuf
syntax = "proto3";
package vizor_proto_demostration;

service HelloService
{
    rpc Hello (HelloRequest) returns (HelloResponse) {}
    rpc ServerTime (ServerTimeRequest) returns (ServerTimeResponse) {}
}

message HelloRequest 
{
    string name = 1;
}

message HelloResponse 
{
    string message = 1;
}

message ServerTimeRequest {}
message ServerTimeResponse
{
    int64 unixTimeStamp = 1;
    uint32 hours  = 2;
    uint32 minutes = 3;
    uint32 seconds = 4;
    string timezone = 5;
    string location = 6;
}
```
[Click here for proto 3 language specification](https://developers.google.com/protocol-buffers/docs/proto3).

Great! We're done with the dull part, let's roll!

### Generating transport code
**Tip:** you can skip this part because this example repository already contains generated transpot code, but it is **not recommended** .

To start doing this, you need to have an [Infraworld Protobuild](https://github.com/vizor-games/infraworld-protobuild). You can read how to use it in it's [README.md](https://github.com/vizor-games/infraworld-protobuild/blob/master/README.md) file. **Don't forget** to add `python` language to the `protobuild.yml` into the `languages` section because our server will be in python.

As the result, your output directory(`gen_root` parameter in `protobuild.yml`) should look like this:

```
gen_root (protobuild output directory)
|
|---cpp
|    |---vizor_demonstration
|        |---vizor_demonstration.grpc.pb.h
|        |---vizor_demonstration.grpc.pb.hpp
|        |---vizor_demonstration.pb.h
|        |---vizor_demonstration.pb.hpp
|
|---python
|    |---vizor_demonstration
|        |---vizor_demonstration_pb2.py
|        |---vizor_demonstration_pb2_grpc.py
|
|--- ...
```

Copy all files from the `gen_root/cpp/vizor_demonstration` to `path/to/InfraworldRuntimeExample/Source/InfraworldDemo/Wrappers/proto/vizor_demonstration`. Also, you need to copy all generated python files into `path/to/InfraworldRuntimeExample/DemoServer` folder.

### Generating Infraworld Runtime UE4-friendly code
**Tip:** you can skip this part because this example repository already contains generated code for the InfraworldRuntime, but it is **not recommended**.

##### Building the Infraworld Cornerstone
Clone **[this repository](https://github.com/vizor-games/infraworld-cornerstone)**. Remeber that the Cornerstone is written in java so you need `jdk8+` and `maven` installed on your system. Then you need to run `mvn install` under Cornerstone directory. You can then find `infraworld-cornerstone.jar` in the `target` directory.

##### Configuting Infraworld Cornerstone
Create `config.yml` file in same directory with `infraworld-cornerstone.jar` and add the following fields:

```
src_path: 'path/to/proto/files'
dst_path: 'path/to/generated/output/files'
module_name: 'InfraworldDemo'
precompiled_header: ''
wrappers_path: 'Wrappers'
company_name: 'Vizor'
```

**Tip:** For more information about Cornerstone building and configuring read [README.md](https://github.com/vizor-games/infraworld-cornerstone/blob/master/README.md) file.

##### Generating UE4-friendly wrappers
When Cornerstone is being successfully built and configured - you can simply run it by command: `java -jar infraworld-cornerstone.jar`

After generation complete your `dst_path` directory should look like this:

```
generated
└── vizor_demonstration
    ├── VizorDemonstration.cpp
    └── VizorDemonstration.h
```

Copy `VizorDemonstration.h` and `VizorDemonstration.cpp` files to `path/to/InfraworldRuntimeExample/Source/InfraworldDemo`

At this point our example Unreal Engine 4 project have all necessary source files and we are ready to compile and run it!

### Building the UE4 client project
If you're working on windows - you need to generate Visual Studion solution for InfraworldExample project. Right click on `InfraworldDemo.uproject` and select `Generate Project Files` section.

After that, the `InfraworldDemo.sln` file should appear. Open it with the Visual Studio and select `Development Editor` configuration then right click on `InfraworldDemo` project and select `build`.

### Running the demo server
In the `DemoServer` directory you can find all server source files. Run `pip3 install -r Requirements.txt`. **Tip:** Maybe you should run `pip` instead `pip3` (depends on your environment).

After all dependences are installed, you will be ready to run the demo server by executing command: `python3 vizor_demo_server.py`. **Tip:** Maybe you should run `python` instead `python3` (depends on your environment). If the server started successfully you will see output like: 

```
Server Started!
```

**Tip:** The Demo Server by default is using the `50051` port.

### Runing the UE4 client
When you have compiled the UE4 project, and your server is running, you can open `InfraworldDemo.uproject`: just double click on it.

In the Unreal Editor, the default `ThirdPersonExampleMap.umap` should be loaded. You can look at `ThirdPersonCharacter` on the scene and its blueprint `ThirdPersonCharacter.uasset`, this blueprint contains all grpc client logic. As you can see, `OnLeftMouseButtonReleased` and `OnRightButtonReleased` are used to send `HelloRequest` and `ServerTimeRequest`. 

So, you can press `Play` button in Editor and see how it works! 

**Tip:** All responses and grpc errors are being printed on the screen.

### Have any troubles?
Feel free to create an issue or contact us via email:

```
nikita.miroshnichenko@vizor-games.com
roman.chehowski@vizor-games.com

```
