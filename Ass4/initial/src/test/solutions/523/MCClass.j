.source MCClass.java
.class public MCClass
.super java.lang.Object

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
.var 1 is i F from Label0 to Label1
	ldc 0.0
	fstore_1
.var 2 is value I from Label0 to Label1
	iconst_0
	istore_2
Label0:
Label2:
	fload_1
	ldc 4.0
	fcmpl
	ifge Label4
	iconst_1
	goto Label5
Label4:
	iconst_0
Label5:
	ifle Label3
.var 3 is value I from Label0 to Label1
	iconst_2
	istore_3
	iload_3
	invokestatic io/string_of_int(I)Ljava/lang/String;
	invokestatic io/print(Ljava/lang/String;)V
	fload_1
	ldc 1.0
	fadd
	fstore_1
	goto Label2
Label3:
	iload_2
	invokestatic io/string_of_int(I)Ljava/lang/String;
	invokestatic io/print(Ljava/lang/String;)V
Label1:
	return
.limit stack 4
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
