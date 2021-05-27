---
title: iterator
date: 2021-04-16 10:39:21
tags: C++
---

### C++ 自定义iterator

{% asset_img lake-6256628.jpg %}

<!-- More -->

```C++
#ifndef LINKEDLIST_H
#define LINKEDLIST_H

#include "node.h"

#include <utility>

// Do not add any #include statements here.  If you have a convincing need for adding a different `#include` please post in the forum on KEATS.

// TODO your code goes here:
#include <initializer_list>

template<typename T>
class LinkedList{
public:
    Node<T>* head;
    Node<T>* tail;
    int sz;
    // constructor with no parameters
    LinkedList(){
        head = tail = nullptr;
        sz = 0;
    }
    // constructor with initializer list
    LinkedList( std::initializer_list<T> ls ){
        head = tail = nullptr;
        sz = 0;
        // add the elements to list
        for(T a: ls){
            push_back(a);
        }
    }

    // push a data in front of list
    void push_front(T data){
        Node<T> * tmp = new Node<T>(data);
        tmp->next = head;
        if(head != nullptr)
            head->previous = tmp;
        else tail = tmp;
        //update head
        head = tmp;
        sz += 1;
    }

    //get first element in list
    T front(){
      return head->data;
    }

    //push a data in the back of list
    void push_back(T data){
        Node<T> * tmp = new Node<T>(data);
        tmp->previous = tail;
        if(tail != nullptr)
            tail->next = tmp;
        else head = tmp;
        //update tail
        tail = tmp;
        sz += 1;

    }

    //return the last element
    T back(){
         return tail->data;
    }

    NodeIterator<T>  begin(){
        return NodeIterator<T>(head);
    }
    NodeIterator<T> end(){
        return NodeIterator<T>(tail->next);
    }

    //destructor
    ~LinkedList(){
        Node<T> * tmp;
        // free list
        while(head != nullptr){
            tmp = head ->next;
            delete head;
            head = tmp;
        }
        tail = nullptr;
        sz = 0;
    }

    // reverse the list
    void reverse(){

        if(sz <= 1)return;
        Node<T> * tmp = tail;
        Node<T> * t = tmp -> previous ;
        Node<T> * tt = t->previous;
        // reverse the antecedent and successor relationship
        while(t != nullptr){
            tmp->next = t;
            t->previous = tmp;
            tmp = t;
            t = tt;
            if(t != nullptr)
            tt = t->previous;
        }
        tail->previous = nullptr;
        head->next = nullptr;
        //update head pointer and tail pointer
        tmp = head;
        head = tail;
        tail = tmp;
    }

    // return the size of list
    int size(){
        return sz;
    }

    // insert a new data to it
    NodeIterator<T> insert(NodeIterator<T> it,T data){
        Node<T> *cur = it.get();
        Node<T> *tmp = new Node<T>(data);
        // empty list
        if(head == nullptr && tail == nullptr){
            head = tail = tmp;
            sz ++;
            return NodeIterator<T>(tmp);
        }
        // not the end,insert data to list
        if(cur != nullptr){
            tmp->previous = cur->previous;
            tmp->next = cur;
            if(tmp->previous == nullptr){
                head = tmp;
            }else{
                tmp->previous->next = tmp;
            }
            cur->previous = tmp;
        }else{
            tail->next = tmp;
            tmp->previous = tail;
            // update tail pointer
            tail = tmp;
        }

        sz ++;
        return NodeIterator<T>(tmp);
    }

    // erase one node from list
    NodeIterator<T> erase(NodeIterator<T> it){
        Node<T> *cur = it.get();

        // current iterator is the tail of list
        if(cur->next == nullptr){
            //update tail pointer
            tail = cur->previous;
            //empty list
            if(tail == nullptr){
                head = nullptr;
            }else tail->next = nullptr;
            delete cur;
            sz --;
            // return iterator of nullptr
            return NodeIterator<T>(nullptr);
        }else {

            cur->next->previous = cur->previous;
            // current iterator is the head of list
            if(cur->previous == nullptr){
                //update head pointer
                head = cur->next;
                //empty list
                if(head == nullptr)tail = nullptr;
                else head->previous = nullptr;
            }else{
                cur->previous->next = cur->next;
            }
            Node<T> * tmp = cur->next;
            sz --;
            delete cur;
            // return a NodeIterator to what is now element i
            return NodeIterator<T>(tmp);
        }
    }

    //return begin of list
    iterator<T> begin() const {
        return iterator<T>(head);
    }

    // end of list
    iterator<T> end() const {
        return iterator<T>(tail->next);
    }
};

// do not edit below this line

#endif

```





```C++
#ifndef NODE_H
#define NODE_H

#include <iostream>
using std::cout;
using std::cerr;
using std::endl;

// Do not add any #include statements here.  If you have a convincing need for adding a different `#include` please post in the forum on KEATS.

// TODO your code for the Node class goes here:
// (Note the 'NodeIterator' class will report lots of errors until Node exists
template<typename T>
class Node{
public:
    T data;// data
    Node * next;//next Node
    Node * previous;//previous Node
    // constructor
    Node(T data){
        this->data = data;
        this->next = nullptr;
        this->previous = nullptr;
    }



};




template<typename T>
class NodeIterator {
  
private:
    
    Node<T>* current;
    
public:
    

    NodeIterator(Node<T>* currentIn)
        : current(currentIn) {        
    }

    T & operator*() {
        return current->data;
    }

    // TODO: complete the code for NodeIterator here
    //return the next Node
    NodeIterator operator++(){
        if(current != nullptr)
            current = current->next;
        return *this;
    }

    // check whether two iterator is same
    bool operator==(const NodeIterator<T> & nod){
        return this->current == nod.current;
    }

    // check whether two iterator is not same
    bool operator!=(const NodeIterator<T> & nod){
        return this->current != nod.current;
    }

    // return the current pointer
    Node<T> *get(){
        return this->current;
    }
};
template<typename T>
class iterator {
private:
    Node<T> *m_ptr;
public:
    // constructor
    iterator(Node<T>* p = nullptr) :
            m_ptr(p) {
    }

    //get data
    T operator*() const {
        return m_ptr->data;
    }

    Node<T>* operator->() const {
        return m_ptr;
    }

    //return the next Node
    iterator& operator++() {
        m_ptr = m_ptr->next;
        return *this;
    }

    // check whether two iterator is same
    bool operator==(const iterator &arg) const {
        return arg.m_ptr == this->m_ptr;
    }

    // check whether two iterator is not same
    bool operator!=(const iterator &arg) const {
        return arg.m_ptr != this->m_ptr;
    }

};

// do not edit below this line

#endif

```

