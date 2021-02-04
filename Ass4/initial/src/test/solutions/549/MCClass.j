.source MCClass.java
.class public MCClass
.super java.lang.Object
.field static x [F
.field static y [Z
.field static z [Ljava/lang/String;

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label0:
	getstatic MCClass/x [F
	iconst_0
	faload
	invokestatic io/string_of_float(F)Ljava/lang/String;
	invokestatic io/print(Ljava/lang/String;)V
	getstatic MCClass/y [Z
	iconst_0
	baload
	invokestatic io/string_of_bool(Z)Ljava/lang/String;
	invokestatic io/print(Ljava/lang/String;)V
	getstatic MCClass/z [Ljava/lang/String;
	iconst_0
	aaload
	invokestatic io/print(Ljava/lang/String;)V
Label1:
	return
.limit stack 2
.limit locals 1
.end method

.method public <clinit>()V
	iconst_1
	newarray float
	dup
	iconst_0
	ldc 3.5
	fastore
	putstatic MCClass/x [F
	iconst_1
	newarray boolean
	dup
	iconst_0
	iconst_1
	bastore
	putstatic MCClass/y [Z
	iconst_1
	anewarray java/lang/String
	dup
	iconst_0
	ldc "Hello"
	aastore
	putstatic MCClass/z [Ljava/lang/String;
	return
.limit stack 7
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
