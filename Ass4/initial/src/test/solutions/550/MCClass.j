.source MCClass.java
.class public MCClass
.super java.lang.Object

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
.var 1 is x [F from Label0 to Label1
	iconst_1
	newarray float
	dup
	iconst_0
	ldc 3.5
	fastore
	astore_1
.var 2 is y [Z from Label0 to Label1
	iconst_1
	newarray boolean
	dup
	iconst_0
	iconst_1
	bastore
	astore_2
.var 3 is z [Ljava/lang/String; from Label0 to Label1
	iconst_1
	anewarray java/lang/String
	dup
	iconst_0
	ldc "Hello"
	aastore
	astore_3
Label0:
	aload_1
	iconst_0
	faload
	invokestatic io/string_of_float(F)Ljava/lang/String;
	invokestatic io/print(Ljava/lang/String;)V
	aload_2
	iconst_0
	baload
	invokestatic io/string_of_bool(Z)Ljava/lang/String;
	invokestatic io/print(Ljava/lang/String;)V
	aload_3
	iconst_0
	aaload
	invokestatic io/print(Ljava/lang/String;)V
Label1:
	return
.limit stack 7
.limit locals 4
.end method

.method public <clinit>()V
	return
.limit stack 0
.limit locals 0
.end method

.method public <init>()V
.var 0 is this LMCClass; from Label0 to Label1
Label0:
	aload_0
	invokespecial java/lang/Object/<init>()V
Label1:
	return
.limit stack 1
.limit locals 1
.end method
