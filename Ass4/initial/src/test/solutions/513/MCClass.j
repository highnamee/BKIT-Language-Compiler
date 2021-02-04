.source MCClass.java
.class public MCClass
.super java.lang.Object
.field static x F
.field static y F

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label0:
	ldc 1.0
	iconst_2
	i2f
	iconst_3
	i2f
	fmul
	fadd
	iconst_4
	i2f
	fsub
	iconst_3
	i2f
	iconst_2
	i2f
	fdiv
	fadd
	invokestatic io/string_of_float(F)Ljava/lang/String;
	invokestatic io/print(Ljava/lang/String;)V
Label1:
	return
.limit stack 3
.limit locals 1
.end method

.method public <clinit>()V
	ldc 2.0
	putstatic MCClass/x F
	ldc 3.0
	putstatic MCClass/y F
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
