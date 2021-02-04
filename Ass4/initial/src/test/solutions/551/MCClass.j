.source MCClass.java
.class public MCClass
.super java.lang.Object

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
.var 1 is a [I from Label0 to Label1
	iconst_3
	newarray int
	dup
	iconst_0
	iconst_1
	iastore
	dup
	iconst_1
	iconst_2
	iastore
	dup
	iconst_2
	iconst_3
	iastore
	astore_1
.var 2 is b I from Label0 to Label1
	iconst_0
	istore_2
Label0:
	aload_1
	iload_2
	invokestatic MCClass/foo([II)V
	aload_1
	iconst_0
	iaload
	invokestatic io/string_of_int(I)Ljava/lang/String;
	invokestatic io/print(Ljava/lang/String;)V
	aload_1
	iconst_1
	iaload
	invokestatic io/string_of_int(I)Ljava/lang/String;
	invokestatic io/print(Ljava/lang/String;)V
	aload_1
	iconst_2
	iaload
	invokestatic io/string_of_int(I)Ljava/lang/String;
	invokestatic io/print(Ljava/lang/String;)V
	iload_2
	invokestatic io/string_of_int(I)Ljava/lang/String;
	invokestatic io/print(Ljava/lang/String;)V
Label1:
	return
.limit stack 4
.limit locals 3
.end method

.method public static foo([II)V
.var 0 is a [I from Label0 to Label1
.var 1 is b I from Label0 to Label1
Label0:
	aload_0
	iconst_0
	iconst_4
	iastore
	aload_0
	iconst_1
	iconst_5
	iastore
	aload_0
	iconst_2
	bipush 6
	iastore
	iconst_1
	istore_1
Label1:
	return
.limit stack 5
.limit locals 2
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
