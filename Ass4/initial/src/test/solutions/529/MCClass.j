.source MCClass.java
.class public MCClass
.super java.lang.Object

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
.var 1 is i F from Label0 to Label1
	ldc 0.0
	fstore_1
Label0:
	ldc 6.0
	fstore_1
Label4:
	fload_1
	ldc 0.0
	fcmpl
	ifle Label5
	iconst_1
	goto Label6
Label5:
	iconst_0
Label6:
	ifle Label3
	fload_1
	invokestatic io/string_of_float(F)Ljava/lang/String;
	invokestatic io/print(Ljava/lang/String;)V
Label2:
	fload_1
	ldc 2.0
	fneg
	fadd
	fstore_1
	goto Label4
Label3:
Label1:
	return
.limit stack 4
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