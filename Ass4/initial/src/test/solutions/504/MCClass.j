.source MCClass.java
.class public MCClass
.super java.lang.Object
.field static x I

.method public static y(I)I
.var 0 is t I from Label0 to Label1
.var 1 is a I from Label0 to Label1
	iconst_3
	istore_1
.var 2 is b I from Label0 to Label1
	iconst_4
	istore_2
Label0:
	iconst_3
	istore_0
	iconst_3
	ireturn
Label1:
.limit stack 1
.limit locals 3
.end method

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label0:
Label1:
	return
.limit stack 0
.limit locals 1
.end method

.method public <clinit>()V
	iconst_2
	putstatic MCClass/x I
	return
.limit stack 1
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
