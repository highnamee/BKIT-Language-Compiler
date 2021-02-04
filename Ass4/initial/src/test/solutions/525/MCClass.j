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
	invokestatic io/string_of_float(F)Ljava/lang/String;
	invokestatic io/print(Ljava/lang/String;)V
	fload_1
	ldc 2.0
	fadd
	fstore_1
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
	goto Label2
Label3:
Label6:
	fload_1
	invokestatic io/string_of_float(F)Ljava/lang/String;
	invokestatic io/print(Ljava/lang/String;)V
	fload_1
	ldc 2.0
	fadd
	fstore_1
	fload_1
	ldc 4.0
	fcmpl
	ifge Label8
	iconst_1
	goto Label9
Label8:
	iconst_0
Label9:
	ifle Label7
	goto Label6
Label7:
Label1:
	return
.limit stack 5
.limit locals 3
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
