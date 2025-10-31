# Defensive Programming

## Introduction

Defensive programming is a methodology aimed at building resilient and predictable code.

In distributed systems and client-server architectures, errors can occur due to latency, partial failures, and unexpected data — defensive techniques ensure that the system remains correct and recoverable.

---

# Programming Concepts

* Correctness: Code should meet its specifications under all valid inputs.
* Complexity: Keep algorithms efficient and the codebase simple.
* Flexibility: Write modular, reusable components that can evolve.
* Use Cases: Define concrete user stories to clarify expected behavior.

## User Stories

Use cases and user stories describe *what the user wants to do* and *why*, helping designers and developers understand functional requirements and user behavior.

### Examples

#### General

1. *As a shopper, I want to save items to a wishlist so that I can buy them later.*
2. *As a new user, I want to sign up with Google so that I don’t have to create a new password.*
3. *As a team manager, I want to export my team’s activity data so that I can analyze performance offline.*

#### Detailed

1. Name: “Add item to cart”  
   Actor: Shopper  
   Precondition: User is logged in and viewing a product.  
   Flow:
   1. User clicks “Add to Cart.”
   2. System adds the item to the active shopping cart.
   3. System updates the cart icon count and shows confirmation.
      Alternate Flow: If item is out of stock, system displays an error message.

2. Name: “Reset Password”  
   Actor: Registered user  
   Flow:  
   1. User clicks “Forgot Password.”
   2. System prompts for email.
   3. User receives a reset link and sets a new password.

### Security Prespective
* Abuse/misuse cases (for identifying and mitigating attacks)

#### Example

Attacker tries to brute-force login credentials.

- Threat: Repeated failed login attempts.
-  Mitigation: Implement rate limiting and temporary account lockout.

---

# Object-Oriented Programming (OOP)

### Core Concepts

* Class: Blueprint for objects.
* Object: Instance of a class.
* Encapsulation: Hide internal state behind public methods.
* Inheritance: Reuse and extend base functionality.
* Polymorphism: Common interface, different implementations.

### UML

Used to visualize class structure and relationships.

### Data Flow Diagram

Visual representation of how data moves through a system.
It shows where data comes from, where it goes, and how it’s transformed.

```
[User] --> (Login Process) --> [Database]
```

### Code Example

* Abstract base class `Shape`.
* Derived `Circle` overriding `area()`.
* Use of virtual destructor.
* Polymorphism through base pointer.

```cpp
class Shape {
public:
    virtual double area() const = 0; // abstract
    virtual ~Shape() = default;
};

class Circle : public Shape {
private:
    double radius;
public:
    explicit Circle(double r): radius(r) {}
    double area() const override { return 3.1415 * radius * radius; }
};

int main() {
    Shape* shape = new Circle(5.0);   // dynamic polymorphism
    std::cout << "Circle area: " << shape->area() << std::endl;
    delete shape;                     // clean up
    return 0;
}
```

---

# C++ (aka Cpp)

## Basics

Cpp is a compiled language that combines low-level memory control with high-level abstractions.

Imporant note: It has no garbage collector, so it is up to the user to plan objects destruction and memory cleanup.

```cpp
#include <iostream>
#include <string>
#include <cstdint>
#include <algorithm>

int main() {
    // Well-defined number types. 
    uint8_t age = 25;
    uint32_t salary = 100000;
    uint32_t max = std::max(1,3);
    uint32_t min = std::min(1,3);

    // I/O
    std::cout << "Age: " << age << std::endl;
    std::cout << "Salary: " << salary << std::endl;

    std::string name;
    std::cout << "Enter your name: ";
    std::cin >> name;
    // Also valid: std::getline(std::cin, name);
    std::cout << "Hello, " << name << "!" << std::endl;

    // foreach 
    std::vector<int> nums = {1, 2, 3, 4, 5};
    for (int value : nums) { 
        std::cout << value << " ";
    }
    std::cout << std::endl;

    // strings
    std::string text = "hello world";
    // length()
    std::cout << "Length: " << text.length() << std::endl;
    // substr()
    std::string sub = text.substr(0, 5); // "hello"
    // find()
    size_t pos = text.find("world");
    if (pos != std::string::npos) {
        std::cout << "'world' found at position " << pos << std::endl;
    }

    // numbers <--> strings
    int num = 42;
    std::string str = std::to_string(num);

    std::string text = "123";
    int n = std::stoi(text);
    double d = std::stod("3.14");
}
```

--- 

## Cpp Runtime Memory Layout — Stack, Heap, Code, and Growth Direction

When a Cpp program runs, memory is divided into regions:

| Region                      | Purpose                                                         | Example                                         |
| --------------------------- | --------------------------------------------------------------- | ----------------------------------------------- |
| Code / Text Segment     | Stores compiled instructions (functions).                       | `main()` machine code lives here.               |
| Static / Global Segment | Stores global and static variables.                             | `static int counter = 0;`                       |
| Heap                    | Dynamically allocated memory (`new`, `malloc`, smart pointers). | `int* p = new int(10);`                         |
| Stack                   | Function calls, local variables, return addresses.              | Inside `main()`, local `int x = 5;` lives here. |

### Growth Direction

* Stack grows downward (toward lower memory addresses).
* Heap grows upward (toward higher addresses).
  They expand toward each other — a full memory collision = stack/heap overflow.

```
| high addresses |
+----------------+
|   Stack (↓)    |
|----------------|
|      ...       |
|----------------|
|   Heap (↑)     |
+----------------+
| low addresses  |
```

---

## Endianness: Little Endian Explained

Little Endian means the least significant byte (LSB) is stored first (at the lowest address).

Example:

```cpp
int x = 0x12345678;
```

Memory layout (addresses increasing →):

```
78 56 34 12
```

Big Endian would store:

```
12 34 56 78
```

Most modern PCs (x86, ARM) are Little Endian.

---

## Manual Memory Management - `new` / `delete`

```cpp
#include <iostream>

int main() {
    int* num = new int(42); // allocate memory
    std::cout << "Value: " << *num << std::endl;

    *num = 100;             // modify value
    std::cout << "New Value: " << *num << std::endl;

    delete num;             // free memory
    num = nullptr;          // avoid dangling pointer

    Dog* d = new Dog(); // create object on heap
    d->bark();
    delete d;           // must delete manually

    return 0;
}
```

---

## References, Move, and Smart Pointers

| Term                                 | Definition                                                                                          | Example                              |
| ------------------------------------ | --------------------------------------------------------------------------------------------------- | ------------------------------------ |
| lvalue reference (`T&`)          | Refers to an existing object (has address).                                                         | `int x = 5; int& r = x;`             |
| rvalue reference (`T&&`)         | Refers to a temporary or movable value. Used for move semantics.                                    | `int&& temp = 10;`                   |
| `std::move`                      | Casts an lvalue to an rvalue reference, allowing resources to be moved.                             | `vec2 = std::move(vec1);`            |
| Smart pointer vs Regular pointer | Smart pointers manage memory automatically; raw pointers require manual `delete` - Shouldn't be used together to avoid bugs.                   | `new/delete` vs `std::unique_ptr`    |
| `std::unique_ptr`                | Smart pointer that owns an object exclusively (no copies). Automatically deletes when out of scope. | `auto p = std::make_unique<int>(5);` |
| `std::shared_ptr`                | Smart pointer that uses reference counting; multiple owners.                                        | `auto p = std::make_shared<int>(5);` |

### `std::unique_ptr` Example

```cpp
#include <memory>
#include <iostream>

struct Node {
    int value;
    explicit Node(int v): value(v) {}
};

int main() {
    std::unique_ptr<Node> ptr = std::make_unique<Node>(42);
    std::cout << ptr->value << std::endl;
    // In order to pass value - pointer must be moved.
    // From now on ptr can't be used - points to nothing.
    std::unique_ptr<Node> ptr2 = std::move(ptr);
    std::cout << ptr2->value << std::endl;

    // Can also be given a "raw" pointer.
    std::unique_ptr<Node> ptr2(new Node(43));
}
```

### `std::shared_ptr` Example

```cpp
#include <memory>
#include <iostream>

struct Resource {
    ~Resource() { std::cout << "Freed\n"; }
};

int main() {
    std::shared_ptr<Resource> r1 = std::make_shared<Resource>();
    std::shared_ptr<Resource> r2 = r1;
    std::cout << "Use count: " << r1.use_count() << std::endl;
}
```

---

## Classes 
- `const` function - means that object properties cannot be changed.
  `const` reference to object - only `const` functions can be used.
- Use public inheritence because then your users can use the public members of the moether class.

```cpp
#include <iostream>
#include <cstring>
#include <string>

// ---------------- Base Abstract Class ----------------
class Printable {
public:
    // Abstract (pure virtual)
    virtual void print() const = 0;
    virtual ~Printable() = default;
};

// ---------------- Buffer Class ----------------
class Buffer : public Printable {
private:
    char* data;
    size_t size;

    // Private functions
    void _allocate(const char* str) {
        size = std::strlen(str);
        data = new char[size + 1];
        std::strcpy(data, str);
    }

public:
    // Constructors - Rule of 5
    // Regular (not counted)
    Buffer(const char* str) { _allocate(str); }
    // Copy
    Buffer(const Buffer& other) { _allocate(other.data); }
    // Operator=
    Buffer& operator=(const Buffer& other) {
        if (this != &other) {
            delete[] data;
            _allocate(other.data);
        }
        return *this;
    }
    // Move
    Buffer(Buffer&& other) noexcept : data(other.data), size(other.size) {
        other.data = nullptr;
        other.size = 0;
    }
    // Move operator=
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data;
            data = other.data;
            size = other.size;
            other.data = nullptr;
            other.size = 0;
        }
        return *this;
    }
    // Virtual destructor
    ~Buffer() override { delete[] data; }

    // Overloaded method: one prints, one with prefix
    void print() const override { std::cout << data << std::endl; }
    void print(const std::string& prefix) const { std::cout << prefix << data << std::endl; }

    // Public functions
    const char* c_str() const { return data; }
    size_t length() const { return size; }

    // Friend operators
    friend std::ostream& operator<<(std::ostream& stream, const Buffer& buf) {
        return stream << buf.data;
    }

    friend Buffer operator*(int times, const Buffer& buf) {
        std::string s;
        for (int i = 0; i < times; ++i)
            s += buf.data;
        return Buffer(s.c_str());
    }
};

// ---------------- Derived Class ----------------
class UpperBuffer : public Buffer {
public:
    // Constructors...
    UpperBuffer(const char* str) : Buffer(str) {}    

    void print() const override {
        std::string temp = c_str();
        for (char& c : temp)
            c = std::toupper(c);
        std::cout << temp << std::endl;
    }
};

// ---------------- Usage ----------------
int main() {
    std::cout << "=== Base buffer ===\n";
    Buffer b1("Hello");
    b1.print();

    std::cout << "\n=== Prefix print ===\n";
    b1.print("Prefix: ");

    std::cout << "\n=== Operator * ===\n";
    Buffer b2 = 3 * b1;
    std::cout << b2 << std::endl;

    std::cout << "\n=== Derived class ===\n";
    UpperBuffer ub("hello world");
    ub.print();  // prints uppercase

    return 0;
}
```

## VTABLE — Virtual Function Table

A vtable (virtual table) is a hidden mechanism that Cpp uses to implement runtime polymorphism for classes with virtual functions.

When a class has at least one `virtual` function:

* The compiler generates a vtable — a table of function pointers.
* Each object of that class stores a hidden pointer (`vptr`) to its class’s vtable.
* At runtime, the correct function is called through that table, based on the actual type of the object (not the pointer type).
* The vtable is essentially an array of pointers to functions and is located at offset 0 of the object's memory.

### Example

```cpp
#include <iostream>

class Base {
public:
    virtual void speak() const { std::cout << "Base speaks\n"; }
    virtual ~Base() = default;
};

class Derived : public Base {
public:
    void speak() const override { std::cout << "Derived speaks\n"; }
};

int main() {
    Base* obj = new Derived();
    obj->speak(); // dynamically calls Derived::speak via vtable
    delete obj;
}
```

Output: `Derived speaks`

If there were no `virtual`, it would instead call `Base::speak()` (static binding).
So the vtable enables dynamic dispatch.

In memory, the bytes at `*obj` are the pointer to `Derived::speak()`.

If there were more function their pointers would be at *(obj + 4), *(obj + 8), etc (assuming 32 bit architecture).

--

## Excptions

```cpp
#include <iostream>
#include <exception>
#include <string>

// Custom exception
class MyException : public std::exception {
private:
    std::string message;
public:
    MyException(const std::string& msg) : message(msg) {}

    const char* what() const noexcept override {
        return message.c_str();
    }
};

int main() {
    try {
        std::cout << "Starting program..." << std::endl;

        int scenario = 0;
        std::cin >> scenario;

        if (scenario == 1)
            throw MyException("custom");
        else if (scenario == 2)
            throw std::runtime_error("runtime");
        else if (scenario == 3)
            throw std::exception("generic");
        else if (scenario == 4)
            // This runs but please don't do it.
            throw 1;

        std::cout << "Program finished normally." << std::endl;
    }
    catch (const MyException& e) {
        std::cerr << "[MyException caught] " << e.what() << std::endl;
    }
    catch (const std::runtime_error& e) {
        std::cerr << "[std::runtime_error caught] " << e.what() << std::endl;
    }
    catch (...) {
        std::cerr << "[Unknown exception caught]" << std::endl;
    }

    std::cout << "Program continues after catch." << std::endl;
    return 0;
}
```

-- 

## Environment 
Windows: `_dupenv_s(&variable_value, &value_length, "VARIABLE")`

Linux: `char* variable_value = getenv("VARIABLE")`

---

## Files

```cpp
#include <fstream>
#include <iostream>
#include <string>

int main() {
    // Write to file
    std::ofstream out("example.txt");
    out << "Hello, file!" << std::endl;
    out.close();

    // Read from file
    std::ifstream in("example.txt");
    std::string line;
    while (std::getline(in, line))
        std::cout << line << std::endl;
    in.close();
}
```

## `std::map` — Key–Value Operations

```cpp
#include <iostream>
#include <map>
#include <string>

int main() {
    // === 1. Constructors ===
    std::map<std::string, int> ages;  // empty map

    // Initializer list constructor
    std::map<std::string, int> scores = {
        {"Alice", 90},
        {"Bob", 85},
        {"Charlie", 95}
    };

    // Copy constructor
    std::map<std::string, int> copyScores(scores);

    // === 2. Insert and Assign ===
    // Cpp17 insert_or_assign - always updates value (even if exists)
    ages.insert_or_assign("Tom", 31);
    ages.insert_or_assign("Spike", 40);

    // === 3. Access ===
    std::cout << "\nAccess by key:" << std::endl;
    // at() throws exception if key not found - better than []
    std::cout << "Tom: " << ages.at("Tom") << std::endl;

    // === 4. Iteration ===
    std::cout << "\nAll entries:" << std::endl;
    for (const auto& items : ages)
        std::cout << items.first << " -> " << items.second << std::endl;

    // === 5. Find and Erase ===
    auto it = ages.find("Spike");
    if (it != ages.end()) {
        std::cout << "\nErasing: " << it->first << std::endl;
        ages.erase(it);
    }

    return 0;
}
```

## `std::vector` — Dynamic Array Operations

```cpp
#include <iostream>
#include <vector>
#include <algorithm> // for std::find

int main() {
    // === 1. Constructors ===
    std::vector<int> v1;                   // empty
    std::vector<int> v2(5, 42);            // {42,42,42,42,42}
    std::vector<int> v3 = { 1, 2, 3, 4, 5 }; // initializer list
    std::vector<int> v4(v3.begin(), v3.end()); // copy from range

    // === 2. push_back / emplace_back ===
    v1.push_back(10);
    v1.push_back(20);
    v1.emplace_back(30);  // constructs in-place

    std::cout << "v1 contents: ";
    for (int x : v1) std::cout << x << " ";
    std::cout << std::endl;

    // === 3. Access ===
    // at() is better than [] - throws std::out_of_range on error
    std::cout << "Second element (at()): " << v3.at(1) << std::endl;

    // === 4. Iteration ===
    std::cout << "v3 elements: ";
    for (auto it = v3.begin(); it != v3.end(); ++it)
        std::cout << *it << " ";
    std::cout << std::endl;

    // === 5. find() ===
    auto it = std::find(v3.begin(), v3.end(), 3);
    if (it != v3.end())
        std::cout << "Found 3 at index " << (it - v3.begin()) << std::endl;

    // === 6. Append another vector ===
    std::vector<int> chunk = { 6, 7, 8 };
    v3.insert(v3.end(), chunk.begin(), chunk.end());
    std::cout << "After append: ";
    for (int x : v3) std::cout << x << " ";
    std::cout << std::endl;

    // === 7. Erase elements ===
    v3.erase(v3.begin(), v3.begin() + 2);  // erase first two
    std::cout << "After erase first 2: ";
    for (int x : v3) std::cout << x << " ";
    std::cout << std::endl;

    // === 8. Other useful methods ===
    std::cout << "Size: " << v3.size() << std::endl;
    std::cout << "Front: " << v3.front() << ", Back: " << v3.back() << std::endl;

    return 0;
}
```

---

## Networking — Boost.Asio Example

### Server

```cpp
#include <boost/asio.hpp>
#include <iostream>
#include <string>

using boost::asio::ip::tcp;

int main() {
    try {
        boost::asio::io_context io;
        tcp::acceptor acceptor(io, tcp::endpoint(tcp::v4(), 12345));

        std::cout << "Server listening on port 12345...\n";

        for (;;) {
            tcp::socket socket(io);
            acceptor.accept(socket);

            std::cout << "Client connected!\n";

            // Read message from client
            boost::asio::streambuf buf;
            boost::asio::read_until(socket, buf, '\n');
            std::string client_msg = boost::asio::buffer_cast<const char*>(buf.data());
            std::cout << "Received from client: " << client_msg;

            // Reply to client
            std::string response = "Server received: " + client_msg;
            boost::asio::write(socket, boost::asio::buffer(response));
        }
    } catch (std::exception& e) {
        std::cerr << "Server error: " << e.what() << std::endl;
    }
}
```

---

### Client

```cpp
#include <boost/asio.hpp>
#include <iostream>
#include <string>

using boost::asio::ip::tcp;

int main() {
    try {
        boost::asio::io_context io;
        tcp::socket socket(io);
        socket.connect(tcp::endpoint(boost::asio::ip::make_address("127.0.0.1"), 12345));

        std::cout << "Connected to server.\n";

        // Send message
        std::string msg = "Hello from client!\n";
        boost::asio::write(socket, boost::asio::buffer(msg));

        // Read response
        boost::asio::streambuf buf;
        boost::asio::read_until(socket, buf, '\n');
        std::string response = boost::asio::buffer_cast<const char*>(buf.data());
        std::cout << "Response from server: " << response << std::endl;

    } catch (std::exception& e) {
        std::cerr << "Client error: " << e.what() << std::endl;
    }
}
```

### Cryptopp
Download and extract -https://www.cryptopp.com/ -> Downloads

Build and add lib to link libraries, add directory as include directory.

### Boost
Download and extract - https://www.boost.org/releases/latest/

Note: To use `asio` you don't need to build it.

---

# Python

## Docs
https://docs.python.org/3/tutorial

## Examples
```python
import string
import random

# Base Class
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        # Defines what str(obj) returns
        return f"Person(name={self.name}, age={self.age}, traits={self.traits})"

    def __getattr__(self, item):
        # Called *only if* attribute not found normally
        print(f"[__getattr__] '{item}' not found, returning default None")
        return None

    def __getattribute__(self, item):
        # Called for *every* attribute access
        print(f"[__getattribute__] Accessing '{item}'")
        return super().__getattribute__(item)

    def __setattr__(self, key, value):
        # Called for every attribute assignment
        print(f"[__setattr__] Setting '{key}' = {value}")
        super().__setattr__(key, value)


# Derived Class
class Student(Person):
    def __init__(self, name , age, grades):
        super().__init__(name, age)
        self.grades = grades

    def add_grade(self, grade):
        self.grades.append(grade)

    def get_grades(self):
        return self.grades


# Function example
# - Required parameters
# - Optional parameters
# - kwargs - generic arguments in form a,b,c   
# - kwargs - generic arguments in form k1=v1,k2=v2,
def func(name, age=0, *args, kwargs):
    print({"name": name, "age": age, "args": args, "kwargs": kwargs})

# Decorator - a function that gets a function and returns a wrapper function.
def timer_decorator(func):
    def wrapper(*args, kwargs):
        start_time = time.time()
        result = func(*args, kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' executed in {end_time - start_time:.4f} seconds.")
        return result
    return wrapper

def main():
    # Dictionaries 
    details = {"major": "Computer Science", "year": 2}
    year = details["year"]
    for key, value in details.items():
        print(f"{key}={value}")
    
    # Lists
    lst = [1,2,4]
    lst.insert(2, 3)
    lst.append(5)
    print(sum(lst))

    # Strings
    # Constants
    chars = string.ascii_letters + string.digits

    # Random choice
    print(random.choice(chars))

    # Functions
    func("bob")
    func("bob", 1)
    func(name="bob", age=1)
    func("bob", 1, 2, 3, d=4, e=5)
    
    # Objects
    s = Student("Alice", 20, [70, 80])
    s.add_grade(95)        
    print(s.get_grades())

    print("\n--- Access attributes (triggering __getattribute__) ---")
    print(s.name)
    print(s.age)

    print("\n--- Access a missing attribute (trigger __getattr__) ---")
    print(s.non_existent_field)

    print("\n--- Print object (trigger __str__) ---")
    print(s)

    print("===== metaprogramming =====") 
    print(f"Object attributes: {dir(s)}")
    print(f"Object class: {s.__class__}")
    print(f"Object base classes: {s.__class.__.__bases__}")

    # Decorating all the methods of an object:
    # @classmethod
    # def class_method(cls):
    #     for attribute, item in cls.__dict__.items():
    #         if callable(item):
    #             setattr(cls,attr,decorator(item))
    


if __name__ == "__main__":
    main()
```

## Networking 
### Client 
```python
import socket

HOST = "127.0.0.1"
PORT = 1234

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    
    # sendall is better than send - actually sends all information  
    client_socket.sendall("Hello World".encode('utf-8'))
    data = client_socket.recv(1024)
    print(data)
```
### Server - Using threads
```python
import socket
import threading

HOST = "127.0.0.1"
PORT = 5000       

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break  # client disconnected
            message = data.decode('utf-8')
            print(f"[{addr}] {message}")
            conn.sendall(f"Echo: {message}".encode('utf-8'))
    print(f"[DISCONNECT] {addr} disconnected.")


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[LISTENING] Server listening on {HOST}:{PORT}")

    try:
        while True:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    except KeyboardInterrupt:
        print("\n[SERVER SHUTDOWN]")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
```

### Server - Using select

```python
import selectors
import socket
selector = selectors.DefaultSelector()

def accept_client(socket_, mask):
    client_socket, client_address = socket_.accept() 
    print(f"New connection from {client_address}")
    client_socket.setblocking(False)
    selector.register(client_socket, selectors.EVENT_READ, read_client)

def read_client(client_socket, mask):
    data = client_socket.recv(1024)
    if data:
        print(f"Echo: {data}")
        client_socket.sendall(data) 
    else:
        print(f"Closed connection: {client_socket}")
        selector.unregister(client_socket)
        client_socket.close()

server_socket = socket.socket()
server_socket.bind(('localhost', 1234))
server_socket.listen(100)
server_socket.setblocking(False)
selector.register(server_socket, selectors.EVENT_READ, accept_client)

while True:
    events = selector.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask) 

```

---

## Struct — Little Endian Example

```python
import struct

# < means little endian
packed = struct.pack('<L', 123456)
print(packed)

value, = struct.unpack('<L', packed)
print(value)
```

## Security in Python 
- `eval(code)` - runs arbitrary code, dangerous because of potential malicious code injection.
- `input()` - in python 2 it gets user input and is interpreted as code. 
  If a variable `password = 123` exists and the user inputs `password` then the return value will be `123`. `raw_input()` should be used in python 2.
- Pickle module - serializes code, dangerous because an attacker can run code on target (deserilizer) machine

---

# SQL

SQL, or Structured Query Language, is a domain-specific programming language designed for managing and manipulating relational databases. It is the standard language used to interact with and extract information from these databases. 

## Features 
- Relational Database Management Systems (RDBMS): SQL is primarily used with RDBMS, which store data in a structured, tabular format with rows and columns. Examples include MySQL, Oracle, PostgreSQL, and Microsoft SQL Server.

- Standardization: SQL is an ANSI and ISO standard, ensuring a degree of consistency across different database systems, although specific implementations may have proprietary extensions.

### Data Manipulation:
SQL allows users to perform various operations on data, such as:
- Retrieving data: Using SELECT statements to extract specific information based on criteria.
- Inserting data: Using INSERT INTO to add new records to tables.
- Updating data: Using UPDATE to modify existing records.
- Deleting data: Using DELETE to remove records from tables.

### Database Structure Management
SQL can also be used to define and modify the structure of a database, including:
- Creating tables: Using CREATE TABLE to define new tables.
- Modifying tables: Using ALTER TABLE to add, modify, or delete columns.
- Deleting tables: Using DROP TABLE to remove tables from the database.

TODO: useful statements

---

# Security

## Definitions
- Bug - A *bug* is an unintended flaw or error in software that causes it to behave incorrectly.
- Vulnerability - A *vulnerability* is a weakness in software or a system that can be exploited to cause unintended behavior — often leading to unauthorized access, data leaks, or service disruption.
- Exploiting - *Exploiting* (or *an exploit*) is the act or method of taking advantage of a vulnerability to achieve a malicious goal — such as executing arbitrary code or escalating privileges.
- Mitigation - *Mitigation* refers to techniques or controls that reduce the risk or impact of a vulnerability or attack.
- Security - *Security* in a system context means the protection of information and operations against unauthorized access, use, modification, or destruction.
- Reliability - *Reliability* means the system consistently performs its intended functions under expected conditions.
- Privacy - *Privacy* is about protecting personal or sensitive information from being disclosed without consent.
- Run-Time Environment - A *runtime environment* is the context in which a program executes — including the system libraries, memory layout, permissions, and interpreter or virtual machine.
- Sandbox - A *sandbox* is an isolated environment for running code safely, so it can’t affect the rest of the system.

TODO: threat tree

## Buffer Overflow

Writing past array bounds.

Bug? 

### Examples
- When logining in and entering a username, write a long answer so that the password field will be overriden.
- Writing into the vtable of an object so we the actual called function will be differnet
- stack cannary

### Mitigations

- Use `strncpy`, `memcpy_s` in C/Cpp.
- Enable stack canaries and ASLR.
- Use safe containers like `std::string`.

---

## Side-Channel Attacks

Leaking info via timing or power analysis.

Bug?: 

### Examples

### Mitigations

* Use constant-time cryptographic operations.
* Isolate sensitive code (TPM, hardware modules).
- use clock to control random number generation
- get private keys

---

## Denial of Service (DoS)

Flooding server with requests.

Bug?:

### Examples

### Prevention

* Rate limiting.
* Timeouts and circuit breakers (TODO explain)
* Create scalable code - does not require more resources if getting a lot of requests (e.g. `select`, reactor pattern).

---

## SQL Injection


Bug?: Unsanitized user input.

### Examples

### Prevention

* Use parameterized queries (`cursor.execute(query, params)`).
* Validate input types.
* Escape strings safely.

---

## Heap Spraying

Filling heap with attacker-controlled data to predict memory layout.

Bug?: 

### Examples

### Prevention


Prevention:

* Enable ASLR and DEP.
* Use safe allocators.
* Randomize heap structures.

---

## Return Oriented Programming (ROP)

Reusing existing code (gadgets) for malicious execution.

Bug?: 

### Examples

### Prevention

Prevention:

* Enable ASLR and Control Flow Integrity.
* Use non-executable stack/heap.
* Maintain shadow stack integrity.

---

## Remote Code Execution (RCE)

Unsafely executing user-supplied code.

### Examples

code injection

### Prevention

- limit code execution scope - exec(code, globals(), locals())
- Never use `eval` or `exec` on untrusted data.
- Disable imports: `exec(code, {'__builtins__': None}, {})`.
    - Trying to bypass import limit - (2,3).__class__.__base__.__subclasses__()
- Use sandboxing or virtual machines.

Bug?: 

---

# Mitigations

## ASLR 

Address Space Layout Randomization (ASLR) randomizes memory layout (stack, heap, libraries, executable base) so that attackers cannot predict addresses needed for many memory corruption exploits.

### Implementation

- How it works: OS kernel chooses randomized offsets when mapping libraries, heap, stack; combined with other mitigations (NX, DEP) it greatly raises the difficulty of code reuse attacks.
- How to disable it in linux (testing only; disabling in production is unsafe): `echo 0 | sudo tee /proc/sys/kernel/randomize_va_space`) (`echo 1` to enable).

## Analysis (static and dynamic) 

Static analysis examines program code or binaries without executing them (linting, SAT/SMT-based checks, pattern matching).  

Dynamic analysis inspects program behavior at runtime (fuzzing, instrumentation, debuggers, runtime monitoring). Both are analysis methods used to find defects and vulnerabilities.

### Implementation

- Static analysis

  - Tools: linters, type checkers, static analyzers, binary scanners.
  - Strengths: early detection, broad code coverage, no need to run untrusted code.
  - Weaknesses: false positives, limited visibility into runtime behavior and environment-specific bugs.
- Dynamic analysis

  - Tools: fuzzers, sanitizers (ASAN, UBSAN), debuggers, instrumentation frameworks (Pin/DynamoRIO), runtime profilers.
  - Strengths: finds bugs that manifest only at runtime (race conditions, memory corruption).
  - Weaknesses: requires workloads / inputs to exercise code paths; may miss rare paths.
- Sandbox mention

  - Sandboxing complements dynamic analysis: run untrusted code in an isolated environment (VM, container, or instrumented sandbox) to observe behavior safely, gather traces, and run automated dynamic tests like fuzzing without risking host compromise.

## Sandbox 

A sandbox is an isolated execution environment that restricts a program’s access to system resources (files, network, devices, other processes) to limit potential damage from buggy or malicious code.

### Implementation

- Techniques:
  - Process isolation: run code with constrained privileges (chroot, seccomp, capability drops, Windows Job Objects).
  - Split-process / internal-external architecture: separate sensitive operations into a small, privileged “core” process and run untrusted or high-risk logic in a less-privileged external process. Example: some VMs and language runtimes (and the user-mentioned PyPy approach) use out-of-process sandboxes for JIT'd code or foreign code execution.
  - Virtualization: full VMs isolate at the hardware/virtual hardware level — strong isolation but heavier weight.
  - Containers: lighter-weight isolation using kernel namespaces and cgroups; good for process isolation but share a kernel with the host (so kernel vulnerabilities matter).
  - Language runtime sandboxes: restricted interpreters that block specific syscalls or APIs.
- Use-cases:
  - Running browser tabs, plugin code, PDF rendering, online code judge systems, malware analysis labs.
- Tradeoffs:
  - Security vs. convenience: stricter sandboxes reduce functionality. Containers are easier to deploy; VMs provide stronger isolation.

## Control Flow Integrity (CFI) 

Control Flow Integrity enforces that a program’s runtime control-flow (which functions can call which other functions, and which return addresses are valid) follows a precomputed legitimate graph so that memory corruption can’t divert execution to arbitrary locations.

### Implementation

- Variants:

  - Coarse-grained CFI: ensure indirect branches only go to a restricted set of possible targets—lighter weight but less strict.
  - Fine-grained CFI: more precise target sets (per-callsite), stronger but more overhead.
- Shadow stack:

  - A common CFI technique to protect returns: maintain a separate, protected stack of return addresses (the *shadow stack*) that cannot be corrupted by normal buffer-overflow writes. On function return, the runtime compares the actual return address with shadow stack entry; mismatch indicates an attack.
  - Implementation requires compiler support and runtime kernel features to protect the shadow stack memory (e.g., make it non-writable to normal code).
- Deployment:

  - Many modern compilers (clang, gcc) provide CFI options; OSes may also implement kernel-level support (e.g., Intel CET for shadow stack support).

## Code Obfuscation 

Code obfuscation is transforming source or binary code to make it harder to analyze and understand while preserving functionality; primarily used to raise the difficulty/cost of reverse engineering.

### Implementation

- Techniques:

  - Identifier renaming, control-flow flattening, opaque predicates, junk instructions, string encryption, virtualization/translation (translate bytecode into a custom VM).
  - Binary-level obfuscation: packers, anti-debugging tricks, API-hiding.
- Use-cases:

  - Protecting IP, licensing checks, deterring casual reverse engineering.
- Drawbacks:

  - Not a replacement for strong security; determined attackers can deobfuscate. Obfuscation increases maintenance complexity and can introduce bugs or performance penalties.

## Vulnerability Indexes 

Vulnerability indexes are structured systems (scores and taxonomies) used to categorize, prioritize, and compare vulnerabilities across software and time. They help in risk triage and remediation planning.

### Implementation

- Why they exist: to provide a common language for severity, exploitability, and impact so organizations can prioritize fixes and measure progress.
- Examples and components:

  - CVSS (Common Vulnerability Scoring System): numeric score (0–10) that encodes attack vector, complexity, privileges required, user interaction, impact on confidentiality/integrity/availability, and temporal/environmental modifiers.
  - CWE (Common Weakness Enumeration): taxonomy of types of software weaknesses (e.g., CWE-79 Cross-site Scripting, CWE-119 Buffer Overflow). Helps classify root cause and improve secure practices.
- Implementation in processes:

  - Ingest CVE reports, map to CWE categories, use CVSS to set SLAs (e.g., fix CVSS ≥ 7 within X days), and maintain dashboards.

## Non-Executable Stack and Heap 

A non-executable (NX) stack/heap marks memory regions used for data (like stack or heap) as non-executable, preventing code injected into those regions from being executed directly.

### Implementation

- Mechanism:

  - The hardware-supported NX bit (or XD on Intel) marks memory pages as non-executable. The OS enforces this mapping via page table permissions.
- Effect:

  - Stops simple code-injection attacks where shellcode is placed on the stack/heap and then jumped to.
  - Attackers adapt with return-oriented programming (ROP) and other code-reuse techniques, so NX is necessary but not sufficient.
- How to enable:

  - Most modern OSes enable DEP/NX by default. Binaries can be linked with appropriate flags that make data pages non-executable.

## SafeSEH 

SafeSEH (Safe Structured Exception Handling) is a Windows-specific mitigation that restricts exception handler addresses to a validated list in the binary’s load-time table, preventing an attacker from using arbitrary exception handlers to gain control.

### Implementation

- Mechanism:

  - Windows PE executables can include a table of valid exception handlers. When an exception occurs, the OS checks that any handler used is in the table; if not, the handler is rejected.
- Notes:

  - SafeSEH historically applied to 32-bit Windows PE files and required cooperation at link-time. Newer mitigations and 64-bit Windows have different exception handling models and protections.
- Tradeoffs:

  - Helps block certain exploit primitives but must be used with other mitigations (ASLR, DEP, CFI).

## Function Pointer Obfuscation 

Function pointer obfuscation hides or mangles function pointers at runtime so that an attacker who obtains memory cannot easily determine or overwrite the true target functions.

### Implementation

- Techniques:

  - XOR/encrypt function pointers when stored in memory and decrypt them on use.
  - Add per-process/per-instance randomization keys (pointer encoding).
  - Use indirection tables with integrity checks (hash-based validation).
- Tradeoffs:

  - Raises bar for attackers but must be done correctly (key management, protection of decoding routine).
  - Can be combined with CFI and hardware-assisted pointer authentication (e.g., ARM PAC or Intel MPX-like approaches) for stronger guarantees.

## Trusted Platform Module (TPM) 

A Trusted Platform Module (TPM) is a hardware security module (a discrete chip or firmware module) that provides secure cryptographic functions and protected storage for keys, measurements, and attestation — designed to resist software-based attacks.

### Implementation

- Capabilities / APIs:

  - Random number generation: hardware entropy sources for cryptographic randomness.
  - Key generation & storage: create asymmetric keys inside the TPM and keep private keys non-exportable.
  - Digital signatures & encryption: TPM can sign or decrypt using keys that never leave the module.
  - Sealing: bind secrets to platform state (PCRs) so keys or secrets can only be unsealed when the system is in a known good state.
  - Attestation: provide cryptographic proof of boot/measured state (used in secure boot, remote attestation).
- Protection against side channels:

  - The TPM’s isolation reduces the risk that private keys are trivially read by software; however, TPMs can still be subject to sophisticated physical side-channel analysis (power, EM) if an attacker has physical access. TPMs reduce the attack surface for software-based side channels by not exporting sensitive key material.
- Practical uses:

  - Disk encryption key storage (e.g., BitLocker), secure boot chains, attestation for cloud VMs, measured launch of sensitive workloads.
- Security guarantee:

  - The promise is that private keys and certain operations happen inside a hardened module — the module enforces that sensitive material never leaves it in the clear.

## Notes

- Defensive layering is crucial: ASLR + NX + CFI + sandboxing + secure build flags + auditing reduces the probability of successful exploitation.
- Testing: use static/dynamic analysis and sandboxed fuzzing to validate mitigations. Try controlled disabling (e.g., ASLR off) in test environments to reproduce exploits for hardening.
- Risk-based prioritization: vulnerability indexes (CVSS/CWE) help decide which mitigations and patches to deploy first.

---

# Encryption

The process of transforming readable data (*plaintext*) into an unreadable format (*ciphertext*) using a mathematical algorithm and one or more keys.
Its purpose is to protect the confidentiality and integrity of information — ensuring that only authorized parties can access or understand it.

Encryption is broadly divided into two categories: Symmetric and Asymmetric encryption.

## Symmetric Encryption

### Definition

The same key is used for both encryption and decryption.
This means the sender and receiver must both possess the shared secret key beforehand.

### Characteristics

* High performance: Fast and efficient, suitable for large amounts of data.
* Challenge: Securely distributing and managing the shared key.
* Best for: Encrypting bulk data, files, or network traffic once keys are established.

### Common Algorithms

| Algorithm                              | Description                                                                                                                                    |
| -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| AES (Advanced Encryption Standard) | The most widely used symmetric cipher. Supports 128-, 192-, and 256-bit keys. Strong and efficient.                                            |
| ChaCha20                           | A stream cipher designed as an alternative to AES. Fast, secure, and resistant to side-channel attacks. Common in mobile and embedded devices. |
| 3DES (Triple DES)                  | Older standard, less secure today. Superseded by AES.                                                                                          |

### Key Exchange

Since symmetric encryption requires both parties to share a secret key, a secure key exchange mechanism is needed.

Examples:
1. Diffie–Hellman (DH) - parties exchange keys, no other mechanism is required.
2. Using asymetric key - party A creates a symmetric key, sends it encrypted it using public key of party B.  

## Asymmetric Encryption

### Definition

Asymmetric encryption uses a key pair:

* A public key (used to encrypt or verify)
* A private key (used to decrypt or sign)

The keys are mathematically related, but the private key cannot be derived from the public key.

Example algorithm - RSA.

### Characteristics

* Public key can be shared openly — private key must be kept secret.
* Slower than symmetric encryption due to heavy math operations.
* Often used to exchange symmetric keys or verify digital signatures, not encrypt large files directly.

### Applications

1. TLS/SSL (HTTPS) –
   Used during the handshake to:

   * Authenticate the server using a certificate.
   * Exchange a symmetric session key securely.
   * Optionally authenticate the client.

2. Digital Signatures –
   The sender signs a message with their private key, and anyone can verify it using the public key.

### How TLS Uses Both

TLS (used by HTTPS) combines both encryption types:

1. Uses asymmetric encryption (RSA or ECDH) for key exchange and authentication.
2. Then switches to symmetric encryption (AES or ChaCha20) for data transfer, since it’s faster.
