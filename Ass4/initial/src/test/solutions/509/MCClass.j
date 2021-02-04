.source MCClass.java
.class public MCClass
.super java.lang.Object
.field static x I
.field static y I

.method public static foo()V
Label0:
	getstatic MCClass/x I
	invokestatic io/string_of_int(I)Ljava/lang/String;
	invokestatic io/print(Ljava/lang/String;)V
Label1:
	return
.limit stack 1
.limit locals 0
.end method

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
.var 1 is x I from Label0 to Label1
	iconst_5
	istore_1
Label0:
	getstatic MCClass/y I
	istore_1
	iload_1
	invokestatic io/string_of_int(I)Ljava/lang/String;
	invokestatic io/print(Ljava/lang/String;)V
	invokestatic MCClass/foo()V
Label1:
	return
.limit stack 1
.limit locals 2
.end method

.method public <clinit>()V
	iconst_2
	putstatic MCClass/x I
	iconst_3
	putstatic MCClass/y I
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
