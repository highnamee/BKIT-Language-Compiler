.source MCClass.java
.class public MCClass
.super java.lang.Object

.method public static isPrimeNumber(I)Z
.var 0 is x I from Label0 to Label1
Label0:
	iload_0
	iconst_2
	if_icmpne Label4
	iconst_1
	goto Label5
Label4:
	iconst_0
Label5:
	ifgt Label9
	iload_0
	iconst_3
	if_icmpne Label6
	iconst_1
	goto Label7
Label6:
	iconst_0
Label7:
	ifgt Label9
	iconst_0
	goto Label8
Label9:
	iconst_1
Label8:
	ifle Label2
	iconst_1
	ireturn
	goto Label3
Label2:
.var 1 is i I from Label0 to Label1
	iconst_1
	istore_1
.var 2 is mid I from Label0 to Label1
	iconst_0
	istore_2
	iload_0
	iconst_2
	idiv
	iconst_1
	iadd
	istore_2
	iconst_2
	istore_1
Label12:
	iload_1
	iload_2
	if_icmpge Label13
	iconst_1
	goto Label14
Label13:
	iconst_0
Label14:
	ifle Label11
	iload_0
	iload_1
	irem
	iconst_0
	if_icmpne Label17
	iconst_1
	goto Label18
Label17:
	iconst_0
Label18:
	ifle Label15
	iconst_0
	ireturn
	goto Label16
Label15:
Label16:
Label10:
	iload_1
	iconst_1
	iadd
	istore_1
	goto Label12
Label11:
Label3:
	iconst_1
	ireturn
Label1:
.limit stack 15
.limit locals 3
.end method

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
.var 1 is x I from Label0 to Label1
	iconst_0
	istore_1
Label0:
	iconst_2
	istore_1
Label4:
	iload_1
	bipush 20
	if_icmpge Label5
	iconst_1
	goto Label6
Label5:
	iconst_0
Label6:
	ifle Label3
	iload_1
	invokestatic MCClass/isPrimeNumber(I)Z
	ifle Label7
	iload_1
	invokestatic io/string_of_int(I)Ljava/lang/String;
	invokestatic io/print(Ljava/lang/String;)V
	ldc "\n"
	invokestatic io/print(Ljava/lang/String;)V
	goto Label8
Label7:
Label8:
Label2:
	iload_1
	iconst_1
	iadd
	istore_1
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
